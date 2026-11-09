// CrownML — Tensor (bloco 1/5).
// N-dimensional, f64, strides row-major, view sem copia quando possivel.

use std::fmt;

#[derive(Clone)]
pub struct Tensor {
    pub(crate) data: Vec<f64>,
    pub(crate) shape: Vec<usize>,
    pub(crate) strides: Vec<usize>,
}

impl Tensor {
    pub fn new(data: Vec<f64>, shape: Vec<usize>) -> Result<Tensor, String> {
        let size: usize = shape.iter().product();
        if size != data.len() {
            return Err(format!(
                "shape {:?} tem {} elementos, dados tem {}",
                shape, size, data.len()
            ));
        }
        let strides = Self::calc_strides(&shape);
        Ok(Tensor { data, shape, strides })
    }

    pub fn zeros(shape: Vec<usize>) -> Tensor {
        let size: usize = shape.iter().product();
        let strides = Self::calc_strides(&shape);
        Tensor { data: vec![0.0; size], shape, strides }
    }

    pub fn ones(shape: Vec<usize>) -> Tensor {
        let size: usize = shape.iter().product();
        let strides = Self::calc_strides(&shape);
        Tensor { data: vec![1.0; size], shape, strides }
    }

    pub fn from_vec(data: Vec<f64>) -> Tensor {
        let n = data.len();
        Tensor { data, shape: vec![n], strides: vec![1] }
    }

    pub fn randn(shape: Vec<usize>) -> Tensor {
        let size: usize = shape.iter().product();
        let strides = Self::calc_strides(&shape);
        let mut data = Vec::with_capacity(size);
        let mut i = 0;
        let mut seed: u64 = 0x1234567890abcdef;
        while i < size {
            seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            let u1 = ((seed >> 11) as f64) / ((1u64 << 53) as f64);
            seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            let u2 = ((seed >> 11) as f64) / ((1u64 << 53) as f64);
            let u1 = if u1 < 1e-12 { 1e-12 } else { u1 };
            let r = (-2.0 * u1.ln()).sqrt();
            let theta = 2.0 * std::f64::consts::PI * u2;
            data.push(r * theta.cos());
            i += 1;
            if i < size {
                data.push(r * theta.sin());
                i += 1;
            }
        }
        Tensor { data, shape, strides }
    }

    pub fn shape(&self) -> &[usize] { &self.shape }
    pub fn strides(&self) -> &[usize] { &self.strides }
    pub fn size(&self) -> usize { self.data.len() }
    pub fn ndim(&self) -> usize { self.shape.len() }

    pub fn data(&self) -> &[f64] { &self.data }
    pub fn data_mut(&mut self) -> &mut [f64] { &mut self.data }

    pub fn get(&self, indices: &[usize]) -> f64 {
        let i = self.offset(indices);
        self.data[i]
    }

    pub fn set(&mut self, indices: &[usize], valor: f64) -> Result<(), String> {
        let i = self.offset(indices);
        if i >= self.data.len() {
            return Err(format!("indice fora: {:?}", indices));
        }
        self.data[i] = valor;
        Ok(())
    }

    fn offset(&self, indices: &[usize]) -> usize {
        let mut off = 0;
        for (i, &idx) in indices.iter().enumerate() {
            if i >= self.strides.len() {
                break;
            }
            off += idx * self.strides[i];
        }
        off
    }

    fn calc_strides(shape: &[usize]) -> Vec<usize> {
        let n = shape.len();
        let mut strides = vec![1; n];
        for i in (0..n.saturating_sub(1)).rev() {
            strides[i] = strides[i + 1] * shape[i + 1];
        }
        strides
    }

    pub fn reshape(&self, novo_shape: Vec<usize>) -> Result<Tensor, String> {
        let novo_size: usize = novo_shape.iter().product();
        if novo_size != self.data.len() {
            return Err(format!(
                "reshape {:?} -> {:?}: tamanho mudou ({} -> {})",
                self.shape, novo_shape, self.data.len(), novo_size
            ));
        }
        let strides = Self::calc_strides(&novo_shape);
        Ok(Tensor { data: self.data.clone(), shape: novo_shape, strides })
    }

    pub fn transpose(&self) -> Tensor {
        if self.ndim() < 2 {
            return self.clone();
        }
        let n = self.ndim();
        let mut novo_shape = self.shape.clone();
        novo_shape.swap(n - 1, n - 2);
        let mut out = Tensor::zeros(novo_shape.clone());
        let ult = n - 1;
        let pen = n - 2;
        let dim_pen = self.shape[pen];
        let dim_ult = self.shape[ult];
        for i in 0..dim_pen {
            for j in 0..dim_ult {
                let mut idx_orig = vec![0; n];
                let mut idx_novo = vec![0; n];
                idx_orig[pen] = i;
                idx_orig[ult] = j;
                idx_novo[pen] = j;
                idx_novo[ult] = i;
                for k in 0..n {
                    if k != pen && k != ult {
                        idx_orig[k] = 0;
                        idx_novo[k] = 0;
                    }
                }
                out.set(&idx_novo, self.get(&idx_orig)).ok();
            }
        }
        out
    }

    pub fn slice(&self, inicio: &[usize], fim: &[usize]) -> Result<Tensor, String> {
        if inicio.len() != self.ndim() || fim.len() != self.ndim() {
            return Err("slice: inicio/fim devem ter o mesmo ndim".to_string());
        }
        let mut novo_shape = vec![0; self.ndim()];
        for i in 0..self.ndim() {
            if inicio[i] >= fim[i] || fim[i] > self.shape[i] {
                return Err(format!("slice invalido no eixo {}", i));
            }
            novo_shape[i] = fim[i] - inicio[i];
        }
        let mut out = Tensor::zeros(novo_shape.clone());
        let mut idx = vec![0; self.ndim()];
        for i in 0..out.size() {
            // Calcula indices a partir do offset linear
            let mut rem = i;
            for d in (0..self.ndim()).rev() {
                idx[d] = rem % novo_shape[d];
                rem /= novo_shape[d];
            }
            let mut idx_orig = vec![0; self.ndim()];
            for d in 0..self.ndim() {
                idx_orig[d] = idx[d] + inicio[d];
            }
            out.data[i] = self.get(&idx_orig);
        }
        Ok(out)
    }

    pub fn sum(&self) -> f64 {
        self.data.iter().sum()
    }

    pub fn mean(&self) -> f64 {
        if self.data.is_empty() { 0.0 } else { self.sum() / self.data.len() as f64 }
    }

    pub fn max(&self) -> f64 {
        self.data.iter().cloned().fold(f64::NEG_INFINITY, f64::max)
    }

    pub fn min(&self) -> f64 {
        self.data.iter().cloned().fold(f64::INFINITY, f64::min)
    }

    pub fn std(&self) -> f64 {
        if self.data.len() < 2 { return 0.0; }
        let m = self.mean();
        let var: f64 = self.data.iter().map(|x| (x - m).powi(2)).sum::<f64>()
            / (self.data.len() - 1) as f64;
        var.sqrt()
    }
}

impl fmt::Display for Tensor {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Tensor(shape={:?}, size={})", self.shape, self.data.len())
    }
}

impl fmt::Debug for Tensor {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Display::fmt(self, f)
    }
}

#[cfg(test)]
mod testes {
    use super::*;

    #[test]
    fn t01_zeros() {
        let t = Tensor::zeros(vec![2, 3]);
        assert_eq!(t.shape(), &[2, 3]);
        assert_eq!(t.size(), 6);
    }

    #[test]
    fn t02_ones() {
        let t = Tensor::ones(vec![2, 3]);
        assert_eq!(t.sum(), 6.0);
    }

    #[test]
    fn t03_from_vec() {
        let t = Tensor::from_vec(vec![1.0, 2.0, 3.0, 4.0]);
        assert_eq!(t.shape(), &[4]);
        assert_eq!(t.get(&[0]), 1.0);
        assert_eq!(t.get(&[3]), 4.0);
    }

    #[test]
    fn t04_get() {
        let t = Tensor::new(vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0], vec![2, 3]).unwrap();
        assert_eq!(t.get(&[0, 0]), 1.0);
        assert_eq!(t.get(&[0, 2]), 3.0);
        assert_eq!(t.get(&[1, 0]), 4.0);
        assert_eq!(t.get(&[1, 2]), 6.0);
    }

    #[test]
    fn t05_set() {
        let mut t = Tensor::zeros(vec![2, 2]);
        t.set(&[0, 1], 99.0).unwrap();
        assert_eq!(t.get(&[0, 1]), 99.0);
    }

    #[test]
    fn t06_reshape_ok() {
        let t = Tensor::from_vec(vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0]);
        let r = t.reshape(vec![2, 3]).unwrap();
        assert_eq!(r.shape(), &[2, 3]);
        assert_eq!(r.get(&[0, 2]), 3.0);
    }

    #[test]
    fn t07_reshape_errado() {
        let t = Tensor::from_vec(vec![1.0, 2.0, 3.0]);
        assert!(t.reshape(vec![2, 2]).is_err());
    }

    #[test]
    fn t08_transpose() {
        let t = Tensor::new(vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0], vec![2, 3]).unwrap();
        let tr = t.transpose();
        assert_eq!(tr.shape(), &[3, 2]);
        assert_eq!(tr.get(&[0, 0]), 1.0);
        assert_eq!(tr.get(&[0, 1]), 4.0);
        assert_eq!(tr.get(&[2, 0]), 3.0);
        assert_eq!(tr.get(&[2, 1]), 6.0);
    }

    #[test]
    fn t09_slice() {
        let t = Tensor::new(vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0], vec![2, 3]).unwrap();
        let s = t.slice(&[0, 0], &[2, 2]).unwrap();
        assert_eq!(s.shape(), &[2, 2]);
        assert_eq!(s.get(&[0, 0]), 1.0);
        assert_eq!(s.get(&[0, 1]), 2.0);
        assert_eq!(s.get(&[1, 0]), 4.0);
        assert_eq!(s.get(&[1, 1]), 5.0);
    }

    #[test]
    fn t10_sum_mean() {
        let t = Tensor::from_vec(vec![1.0, 2.0, 3.0, 4.0]);
        assert_eq!(t.sum(), 10.0);
        assert_eq!(t.mean(), 2.5);
    }

    #[test]
    fn t11_max_min() {
        let t = Tensor::from_vec(vec![3.0, 1.0, 4.0, 1.0, 5.0, 9.0, 2.0, 6.0]);
        assert_eq!(t.max(), 9.0);
        assert_eq!(t.min(), 1.0);
    }

    #[test]
    fn t12_randn() {
        let t = Tensor::randn(vec![1000]);
        let m = t.mean();
        let s = t.std();
        assert!(m.abs() < 0.2, "media {} fora", m);
        assert!((s - 1.0).abs() < 0.2, "std {} fora", s);
    }
}
