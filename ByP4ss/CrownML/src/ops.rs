// CrownML — Ops (bloco 2/5).
// Elementwise, broadcasting, matmul, ativacoes, reducao com eixo.

use crate::tensor::Tensor;

fn calc_strides(shape: &[usize]) -> Vec<usize> {
    let n = shape.len();
    let mut strides = vec![1; n];
    for i in (0..n.saturating_sub(1)).rev() {
        strides[i] = strides[i + 1] * shape[i + 1];
    }
    strides
}

fn broadcast_shapes(a: &[usize], b: &[usize]) -> Result<Vec<usize>, String> {
    let n = a.len().max(b.len());
    let mut out = vec![0; n];
    for i in 0..n {
        let da = if i < n - a.len() { 1 } else { a[i - (n - a.len())] };
        let db = if i < n - b.len() { 1 } else { b[i - (n - b.len())] };
        if da == db || da == 1 || db == 1 {
            out[i] = da.max(db);
        } else {
            return Err(format!("broadcast impossivel: {:?} com {:?}", a, b));
        }
    }
    Ok(out)
}

fn get_broadcast(t: &Tensor, idx: &[usize], shape: &[usize]) -> f64 {
    let t_ndim = t.ndim();
    let s_ndim = shape.len();
    let offset = s_ndim - t_ndim;
    let mut idx_local = vec![0; t_ndim];
    for i in 0..t_ndim {
        let dim_size = t.shape()[i];
        let idx_global = idx[i + offset];
        idx_local[i] = if dim_size == 1 { 0 } else { idx_global };
    }
    t.get(&idx_local)
}

fn elementwise(a: &Tensor, b: &Tensor, f: impl Fn(f64, f64) -> f64) -> Result<Tensor, String> {
    let shape = broadcast_shapes(a.shape(), b.shape())?;
    let mut out = Tensor::zeros(shape.clone());
    let size = out.size();
    let ndim = shape.len();
    let mut idx = vec![0; ndim];
    for i in 0..size {
        let mut rem = i;
        for d in (0..ndim).rev() {
            idx[d] = rem % shape[d];
            rem /= shape[d];
        }
        let va = get_broadcast(a, &idx, &shape);
        let vb = get_broadcast(b, &idx, &shape);
        out.data_mut()[i] = f(va, vb);
    }
    Ok(out)
}

pub fn add(a: &Tensor, b: &Tensor) -> Result<Tensor, String> {
    elementwise(a, b, |x, y| x + y)
}
pub fn sub(a: &Tensor, b: &Tensor) -> Result<Tensor, String> {
    elementwise(a, b, |x, y| x - y)
}
pub fn mul(a: &Tensor, b: &Tensor) -> Result<Tensor, String> {
    elementwise(a, b, |x, y| x * y)
}
pub fn div(a: &Tensor, b: &Tensor) -> Result<Tensor, String> {
    elementwise(a, b, |x, y| x / y)
}

pub fn add_scalar(a: &Tensor, s: f64) -> Tensor {
    let mut out = a.clone();
    for v in out.data_mut().iter_mut() { *v += s; }
    out
}
pub fn mul_scalar(a: &Tensor, s: f64) -> Tensor {
    let mut out = a.clone();
    for v in out.data_mut().iter_mut() { *v *= s; }
    out
}

pub fn neg(a: &Tensor) -> Tensor {
    mul_scalar(a, -1.0)
}

pub fn abs(a: &Tensor) -> Tensor {
    let mut out = a.clone();
    for v in out.data_mut().iter_mut() { *v = v.abs(); }
    out
}

pub fn pow(a: &Tensor, e: f64) -> Tensor {
    let mut out = a.clone();
    for v in out.data_mut().iter_mut() { *v = v.powf(e); }
    out
}

pub fn sqrt(a: &Tensor) -> Result<Tensor, String> {
    if a.data().iter().any(|&x| x < 0.0) {
        return Err("sqrt de negativo".to_string());
    }
    let mut out = a.clone();
    for v in out.data_mut().iter_mut() { *v = v.sqrt(); }
    Ok(out)
}

pub fn exp(a: &Tensor) -> Tensor {
    let mut out = a.clone();
    for v in out.data_mut().iter_mut() { *v = v.exp(); }
    out
}

pub fn log(a: &Tensor) -> Result<Tensor, String> {
    if a.data().iter().any(|&x| x <= 0.0) {
        return Err("log de <= 0".to_string());
    }
    let mut out = a.clone();
    for v in out.data_mut().iter_mut() { *v = v.ln(); }
    Ok(out)
}

pub fn matmul(a: &Tensor, b: &Tensor) -> Result<Tensor, String> {
    if a.ndim() != 2 || b.ndim() != 2 {
        return Err(format!("matmul: esperado 2D, veio {:?} e {:?}", a.shape(), b.shape()));
    }
    let (m, k1) = (a.shape()[0], a.shape()[1]);
    let (k2, n) = (b.shape()[0], b.shape()[1]);
    if k1 != k2 {
        return Err(format!("matmul: {:?} @ {:?} incompativeis", a.shape(), b.shape()));
    }
    let mut out = Tensor::zeros(vec![m, n]);
    for i in 0..m {
        for j in 0..n {
            let mut s = 0.0;
            for kk in 0..k1 {
                s += a.get(&[i, kk]) * b.get(&[kk, j]);
            }
            out.set(&[i, j], s).ok();
        }
    }
    Ok(out)
}

pub fn relu(a: &Tensor) -> Tensor {
    let mut out = a.clone();
    for v in out.data_mut().iter_mut() { *v = v.max(0.0); }
    out
}

pub fn sigmoid(a: &Tensor) -> Tensor {
    let mut out = a.clone();
    for v in out.data_mut().iter_mut() { *v = 1.0 / (1.0 + (-*v).exp()); }
    out
}

pub fn tanh(a: &Tensor) -> Tensor {
    let mut out = a.clone();
    for v in out.data_mut().iter_mut() { *v = v.tanh(); }
    out
}

pub fn softmax(a: &Tensor) -> Tensor {
    if a.ndim() < 1 {
        return a.clone();
    }
    let ultimo = a.shape()[a.ndim() - 1];
    let total = a.size() / ultimo;
    let mut out = a.clone();
    let data = out.data_mut();
    for i in 0..total {
        let base = i * ultimo;
        let mut max = f64::NEG_INFINITY;
        for j in 0..ultimo {
            if data[base + j] > max { max = data[base + j]; }
        }
        let mut soma = 0.0;
        for j in 0..ultimo {
            let e = (data[base + j] - max).exp();
            data[base + j] = e;
            soma += e;
        }
        for j in 0..ultimo {
            data[base + j] /= soma;
        }
    }
    out
}

pub fn gelu(a: &Tensor) -> Tensor {
    // Aproximacao tanh do GELU
    let mut out = a.clone();
    let c = (2.0 / std::f64::consts::PI).sqrt();
    for v in out.data_mut().iter_mut() {
        let x = *v;
        *v = 0.5 * x * (1.0 + (c * (x + 0.044715 * x.powi(3))).tanh());
    }
    out
}

pub fn sum_eixo(a: &Tensor, eixo: usize) -> Result<Tensor, String> {
    if eixo >= a.ndim() {
        return Err(format!("eixo {} fora de ndim {}", eixo, a.ndim()));
    }
    let mut novo_shape = a.shape().to_vec();
    novo_shape.remove(eixo);
    if novo_shape.is_empty() {
        return Ok(Tensor::from_vec(vec![a.sum()]));
    }
    let mut out = Tensor::zeros(novo_shape.clone());
    let dim_eixo = a.shape()[eixo];
    let ndim = a.ndim();
    let size = out.size();
    let mut idx_out = vec![0; novo_shape.len()];
    for i in 0..size {
        let mut rem = i;
        for d in (0..novo_shape.len()).rev() {
            idx_out[d] = rem % novo_shape[d];
            rem /= novo_shape[d];
        }
        let mut soma = 0.0;
        for e in 0..dim_eixo {
            let mut idx_a = vec![0; ndim];
            let mut sobra = 0;
            for d in 0..ndim {
                if d == eixo { idx_a[d] = e; }
                else { idx_a[d] = idx_out[sobra]; sobra += 1; }
            }
            soma += a.get(&idx_a);
        }
        out.data_mut()[i] = soma;
    }
    Ok(out)
}

pub fn mean_eixo(a: &Tensor, eixo: usize) -> Result<Tensor, String> {
    let s = sum_eixo(a, eixo)?;
    let n = a.shape()[eixo] as f64;
    Ok(mul_scalar(&s, 1.0 / n))
}

#[cfg(test)]
mod testes {
    use super::*;

    fn t2x3() -> Tensor {
        Tensor::new(vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0], vec![2, 3]).unwrap()
    }

    #[test]
    fn o01_add_same_shape() {
        let a = t2x3();
        let r = add(&a, &a).unwrap();
        assert_eq!(r.shape(), &[2, 3]);
        assert_eq!(r.get(&[0, 0]), 2.0);
        assert_eq!(r.get(&[1, 2]), 12.0);
    }

    #[test]
    fn o02_add_broadcast_vec() {
        let a = t2x3();
        let b = Tensor::from_vec(vec![10.0, 20.0, 30.0]);
        let r = add(&a, &b).unwrap();
        assert_eq!(r.shape(), &[2, 3]);
        assert_eq!(r.get(&[0, 0]), 11.0);
        assert_eq!(r.get(&[0, 2]), 33.0);
        assert_eq!(r.get(&[1, 0]), 14.0);
        assert_eq!(r.get(&[1, 2]), 36.0);
    }

    #[test]
    fn o03_add_broadcast_2d() {
        let a = Tensor::new(vec![1.0, 2.0, 3.0, 4.0], vec![2, 2]).unwrap();
        let b = Tensor::new(vec![10.0, 20.0], vec![1, 2]).unwrap();
        let r = add(&a, &b).unwrap();
        assert_eq!(r.get(&[0, 0]), 11.0);
        assert_eq!(r.get(&[1, 1]), 24.0);
    }

    #[test]
    fn o04_add_incompativel() {
        let a = Tensor::zeros(vec![2, 3]);
        let b = Tensor::zeros(vec![2, 4]);
        assert!(add(&a, &b).is_err());
    }

    #[test]
    fn o05_mul_hadamard() {
        let a = Tensor::from_vec(vec![1.0, 2.0, 3.0]);
        let b = Tensor::from_vec(vec![4.0, 5.0, 6.0]);
        let r = mul(&a, &b).unwrap();
        assert_eq!(r.data(), &[4.0, 10.0, 18.0]);
    }

    #[test]
    fn o06_matmul() {
        let a = Tensor::new(vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0], vec![2, 3]).unwrap();
        let b = Tensor::new(
            vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0],
            vec![3, 4],
        ).unwrap();
        let r = matmul(&a, &b).unwrap();
        assert_eq!(r.shape(), &[2, 4]);
        // 1*1+2*5+3*9 = 1+10+27 = 38
        assert_eq!(r.get(&[0, 0]), 38.0);
        // 1*4+2*8+3*12 = 4+16+36 = 56
        assert_eq!(r.get(&[0, 3]), 56.0);
    }

    #[test]
    fn o07_matmul_incompativel() {
        let a = Tensor::zeros(vec![2, 3]);
        let b = Tensor::zeros(vec![4, 2]);
        assert!(matmul(&a, &b).is_err());
    }

    #[test]
    fn o08_relu() {
        let a = Tensor::from_vec(vec![-1.0, 0.0, 1.0, 2.0]);
        let r = relu(&a);
        assert_eq!(r.data(), &[0.0, 0.0, 1.0, 2.0]);
    }

    #[test]
    fn o09_sigmoid() {
        let a = Tensor::from_vec(vec![0.0, 100.0, -100.0]);
        let r = sigmoid(&a);
        let d = r.data();
        assert!((d[0] - 0.5).abs() < 1e-9);
        assert!((d[1] - 1.0).abs() < 1e-9);
        assert!(d[2].abs() < 1e-9);
    }

    #[test]
    fn o10_softmax() {
        let a = Tensor::from_vec(vec![1.0, 2.0, 3.0]);
        let r = softmax(&a);
        let soma: f64 = r.data().iter().sum();
        assert!((soma - 1.0).abs() < 1e-9, "soma {}", soma);
        let d = r.data();
        assert!(d[0] < d[1] && d[1] < d[2]);
    }
}
