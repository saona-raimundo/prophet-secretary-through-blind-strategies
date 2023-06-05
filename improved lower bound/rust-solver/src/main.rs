use num_traits::{
	identities::{Zero, One},
	cast::FromPrimitive,
};

// use ordered_float::{Float, OrderedFloat};
/// Concrete computer representation of a real number 
type Real = f32; //OrderedFloat<f64>;

/// Size of the blind strategy
const M: usize = 30;

/// Detailed performance of the blind strategy. 
///
/// The guarantee is at least the minimum of the return vector.
fn detailed_performance(alpha: &[Real; M]) -> [Real; M + 1] {
	assert_eq!(alpha.len(), M);

	// Initialize
    let m = Real::from_usize(M).expect("M is real");
    let m_inv = m.recip();
    let one = Real::one();
    let zero = Real::zero();
    
    // Detailed factor 
    // g_{m,p}(k), where p = alpha_1
    let g = {
	    let mut g = [zero; M];
	    let p = alpha[0];
	    for k in 1..=M {
	        if k <= M/2 {
	            g[k-1] = ( one - Real::from_usize(k).unwrap() * m_inv * ( one - p ) ).recip();
	        }
	        else {
	            g[k-1] = Real::from_usize(2).unwrap() / ( one + p );
	        }
	    }
	    g
    };

    // Computing garantee
    // f_j( \alpha_1, ..., \alpha_m )
    
    // Initialize
    let mut f = [zero; M + 1];
    // j = 1
    f[0] = (1..=M).map(|k| {
    	alpha[0..(k-1)].iter().product::<Real>().powf(m_inv) 
    		* (one - alpha[k-1].powf(m_inv))
	    	/ -alpha[k-1].ln()
    }).sum();

    // j = m+1
    f[M] = one - alpha.iter().sum::<Real>() * m_inv;


    // j in {2, ..., m}
    // Initial building blocks
    let alpha_cumsum: [Real; M + 1] = {
    	let mut acc = [zero; M + 1];
    	for (i, a) in alpha.iter().enumerate() {
    		acc[i + 1] = acc[i] + a;
    	}
    	acc
    };
    let alpha_cumprod = {
    	let mut acc = [one; M + 1];
    	for (i, a) in alpha.iter().enumerate() {
    		acc[i + 1] = acc[i] * a;
    	}
    	acc
    };
    // Define for each j
    for j in 2..=M {
        let aux = (j..=M).map(|k| {
            let a_k = alpha[k-1];
        	alpha_cumprod[k-1].powf(m_inv) * g[k-2] * (one - a_k.powf(m_inv)) / -a_k.ln()
        });
        f[j-1] = (Real::from_usize(j-1).expect("small usize is real") - alpha_cumsum[j-1]) * m_inv / (one - alpha[j-1])
        	+ aux.into_iter().sum::<Real>()
        	;
    }

    f
}



fn is_admissible(alpha: &[Real; M]) -> bool {
	// domain
	alpha.iter().all(|&a| Real::zero() <= a && a <= Real::one()) 
	&&
	// decreasing
	alpha.windows(2).all(|window: &[Real]| window[0] >= window[1])
} 

use argmin::core::observers::{ObserverMode, SlogLogger};
use argmin::core::{CostFunction, Error, Executor};
use argmin::solver::neldermead::NelderMead;

/// Problem cost function
fn cost(x: &[Real; M]) -> Real {
	if is_admissible(x) {
    	- detailed_performance(x).into_iter().reduce(|a, b| a.min(b)).expect("There are elements")
	} else {
		Real::zero() // an undesirable value
	}
}

/// Problem Definition
/// 
/// minimize cost(x) 
struct Problem;

impl CostFunction for Problem {
    type Param = [Real; M];
    type Output = Real;

    fn cost(&self, x: &Self::Param) -> Result<Self::Output, Error> {
        Ok(cost(x))
    }
}

fn main() {

    let o = detailed_performance(&[0.67699182, 0.66490484, 0.60158186, 0.55614734, 0.52010464,
       0.49025544, 0.46484012, 0.4424727 , 0.4224104 , 0.40415579,
       0.3874404 , 0.37196344, 0.35793043, 0.34318325, 0.32944535,
       0.31320542, 0.29739753, 0.28191541, 0.26670487, 0.25143146,
       0.23601253, 0.22021746, 0.20378073, 0.18680571, 0.16867315,
       0.14915083, 0.12761786, 0.10292822, 0.07331355, 0.03333235]
    );
    println!("{:?}", o);
    println!("{:?}", o.into_iter().reduce(|a, b| a.min(b)));

    // let problem = Problem;
    // let solver = NelderMead::new(vec![[Real::one() / 2.; M], [Real::one() / 3.; M]]);

    // let res = Executor::new(problem, solver)
    //     .configure(|state| state.max_iters(1000))
    //     .add_observer(SlogLogger::term(), ObserverMode::Always)
    //     .run()
    //     .expect("Failed to run optimization");

    // println!("Result:\n{}", res);
}

