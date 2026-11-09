// CrownML — framework de rede neural proprio.
// Rust puro. Sem ndarray, sem nalgebra, sem rayon.
// CPU single-thread. f64.

pub mod tensor;

pub use tensor::Tensor;
pub mod ops;
pub use ops;
