import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class SynthConfig:
    image_shape: Tuple[int, int] = (128, 128)
    lesion_radius_px: int = 3
    doses: int = 11
    contrasts: int = 7
    realizations: int = 10
    recon_types: Tuple[str, str] = ("FBP", "MAR")
    classes: Tuple[str, str] = ("absent", "present")
    base_bg_mean: float = 1000.0
    base_bg_std: float = 20.0
    # Dose scales noise ~ 1/sqrt(dose+1) to keep d=0 finite
    dose_noise_scale: float = 1.0
    contrast_min: float = 1.00
    contrast_max: float = 1.06
    rng_seed: int = 7
    roi_size: Tuple[int, int] = (25, 25)
    channels: int = 16
    lambda_reg: float = 1e-3

def _draw_lesion(img: np.ndarray, center: Tuple[int, int], radius: int, delta: float):
    cx, cy = center
    H, W = img.shape
    y, x = np.ogrid[:H, :W]
    mask = (x - cx)**2 + (y - cy)**2 <= radius**2
    img[mask] = img[mask] * (1.0 + delta)

def _metal_artifact_field(shape, rod_x: int, width: int, strength: float, rng):
    H, W = shape
    field = np.zeros(shape, dtype=float)
    # Streak-like stripes orthogonal to rod, decaying with distance
    for i in range(-3, 4):
        stripe = np.zeros(shape, dtype=float)
        dx = np.abs(np.arange(W) - (rod_x + i * width))
        stripe += (1.0 / (1.0 + dx[None, :]))  # HxW broadcast
        field += stripe
    # normalize and scale
    field = field / (field.max() + 1e-8)
    return strength * field

def generate_synthetic_study(cfg: Dict) -> Dict:
    """Generate synthetic images approximating adult-chest w/ titanium rod scenario.Returns a dict of arrays and meta suitable for ROI extraction & CHO.

Keys:

- 'images' : dict keyed by (dose, contrast, realization, recon, cls) -> image np.ndarray

- 'roi_centers' : list of (y, x)

- 'meta' : configuration details

    """
    sc = SynthConfig(**cfg)
    rng = np.random.default_rng(sc.rng_seed)

    # Derived levels
    dose_levels = np.arange(sc.doses)  # 0..10
    contrast_levels = np.linspace(sc.contrast_min, sc.contrast_max, sc.contrasts)

    H, W = sc.image_shape
    rod_x = W // 2 - 8  # rod near spine
    images = {}

    for d in dose_levels:
        # background noise scaling
        noise_sigma = sc.base_bg_std * sc.dose_noise_scale / np.sqrt(d + 1.0)
        # MAR vs FBP effect flag (e.g., MAR reduces streak amplitude at higher doses)
        for j, c in enumerate(contrast_levels):
            for r in range(sc.realizations):
                # base background
                base = rng.normal(loc=sc.base_bg_mean, scale=noise_sigma, size=sc.image_shape).astype(float)

                # metal artifact pattern (FBP stronger, MAR weaker with residual smoothing)
                artifact_fbp = _metal_artifact_field(sc.image_shape, rod_x=rod_x, width=2, strength=8.0, rng=rng)
                artifact_mar = _metal_artifact_field(sc.image_shape, rod_x=rod_x, width=2, strength=3.0, rng=rng)
                sm = rng.normal(0, 0.5, size=sc.image_shape)
                # recon variants
                fbp_img = base + artifact_fbp + sm
                mar_img = base + artifact_mar + 0.5*sm

                # lesion location (adjacent to rod: 10 px away)
                center = (H//2, rod_x + 10)

                for recon_name, img in (("FBP", fbp_img), ("MAR", mar_img)):
                    # class absent
                    images[(d, j, r, recon_name, "absent")] = img.astype(np.float32, copy=False)
                    # class present: add lesion contrast relative to background
                    lesion_img = img.copy()
                    _draw_lesion(lesion_img, center=center, radius=sc.lesion_radius_px, delta=(c-1.0))
                    images[(d, j, r, recon_name, "present")] = lesion_img.astype(np.float32, copy=False)

    roi_centers = [(H//2, rod_x + 10)]  # lesion-adjacent ROI
    return {
        "images": images,
        "roi_centers": roi_centers,
        "dose_levels": dose_levels.tolist(),
        "contrast_levels": contrast_levels.tolist(),
        "meta": {
            "image_shape": sc.image_shape,
            "classes": sc.classes,
            "recon_types": sc.recon_types,
            "description": "Adult chest, titanium rod (adjacent lesion), synthetic realistic patterns",
        },
    }
