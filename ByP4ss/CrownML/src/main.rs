// CrownML — binario CLI (bloco 1/5: so teste).
use crownml::Tensor;

fn main() {
    println!("CrownML v0.1.0 — bloco 1/5");
    let t = Tensor::zeros(vec![2, 3]);
    println!("zeros(2,3) = shape {:?}, size {}", t.shape(), t.size());
}
