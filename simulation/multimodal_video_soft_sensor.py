"""
Zero-Hardware Multimodal Video + Satellite + Physics Soft-Sensor Assimilator
============================================================================
Replaces expensive in-ground hardware probes on smallholder farms by fusing:
1. Direct Video Frame & Audio Bio-Assays (from YouTube farm walkthroughs or
   15-second smartphone clips: leaf turgor/wilting angle, Munsell soil wetness,
   surface crack width, 1-liter bottle infiltration timing, canopy gap fraction,
   and mound/trench geometry).
2. Physics-Constrained Hype Filter (rejects YouTube/internet yield or zero-water
   claims that violate transpiration Water-Use Efficiency or PAR energy bounds).
3. Bayesian Particle Filter (Sequential Monte Carlo) assimilating 6-day Sentinel-1
   SAR surface wetness + weekly video bio-assays into the 2-layer / L-horizon
   mass-conserving physics engine to recover hidden subsoil moisture (theta_2).
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class VideoFrameBioAssay:
    """
    Quantitative physical observables extracted by a Vision-Language Model (VLM) +
    monocular depth / segmentation (SAM-2 / Depth-Anything) from raw video frames.
    """
    source_video_id: str
    day_index: int
    # 1. Visual topsoil state from video frames (Munsell value/chroma darkening & crack width)
    visual_topsoil_wetness_theta1: float        # Estimated topsoil volumetric moisture (m3/m3)
    topsoil_obs_std: float = 0.025
    # 2. Living-plant tensiometer: leaf drooping/rolling angle & stomatal turgor score in [0, 1]
    visual_canopy_turgor_score: float = 0.85    # 1.0 = full turgor, 0.0 = severe wilting
    turgor_obs_std: float = 0.050
    # 3. Optional 1-liter bottle infiltration bio-assay timed directly from video frames
    bottle_1l_infiltration_seconds: float | None = None
    # 4. Canopy gap fraction & multi-strata architecture measured from video frames
    canopy_gap_fraction: float | None = None
    mound_height_cm_from_depth: float | None = None
    mulch_cover_fraction: float | None = None


def estimate_ksat_from_bottle_video(infiltration_seconds: float, ring_diameter_cm: float = 10.0) -> float:
    """
    Convert a 1-liter (1000 cm3) pour infiltration time observed in a video clip
    into effective saturated hydraulic conductivity Ksat (mm/day) via Falling-Head
    Green-Ampt scaling.
    """
    area_cm2 = np.pi * ((ring_diameter_cm / 2.0) ** 2)
    depth_mm = (1000.0 / max(area_cm2, 1.0)) * 10.0
    rate_mm_sec = depth_mm / max(infiltration_seconds, 5.0)
    # Apply sorptivity-to-gravity conversion factor (0.18) and cap to physical bounds
    ksat_est = rate_mm_sec * 86400.0 * 0.0025
    return float(np.clip(ksat_est, 2.0, 250.0))


def invert_lai_from_video_gap_fraction(gap_fraction: float, k_extinction: float = 0.55) -> float:
    """Invert Beer-Lambert canopy gap fraction P_0 = exp(-k * LAI) from upward/oblique video frames."""
    g = float(np.clip(gap_fraction, 0.03, 0.98))
    return float(np.clip(-np.log(g) / max(k_extinction, 0.1), 0.1, 6.5))


def verify_youtube_yield_claim_against_physics(
    claimed_dry_biomass_kg_ha: float,
    seasonal_transpiration_mm: float,
    seasonal_par_mj_m2: float = 950.0,
    max_wue_kg_ha_per_mm: float = 22.0,
    max_rue_g_per_mj: float = 2.8,
) -> dict[str, object]:
    """
    Adversarial Physics Gate (Murphy + Aris):
    Audit whether a yield claim mined from a YouTube video or web article is
    thermodynamically and hydrologically possible under the farm's water & solar budget.
    """
    water_ceiling_kg_ha = seasonal_transpiration_mm * max_wue_kg_ha_per_mm
    radiation_ceiling_kg_ha = seasonal_par_mj_m2 * max_rue_g_per_mj * 10.0  # 1 g/m2 = 10 kg/ha
    physical_ceiling = min(water_ceiling_kg_ha, radiation_ceiling_kg_ha)
    plausible = bool(claimed_dry_biomass_kg_ha <= physical_ceiling * 1.05)
    return {
        "claimed_dry_biomass_kg_ha": round(claimed_dry_biomass_kg_ha, 1),
        "water_limited_ceiling_kg_ha": round(water_ceiling_kg_ha, 1),
        "radiation_limited_ceiling_kg_ha": round(radiation_ceiling_kg_ha, 1),
        "physically_plausible": plausible,
        "assigned_evidence_class": "VIDEO_OBSERVED_PLAUSIBLE" if plausible else "REJECTED_PROMOTIONAL_OUTLIER",
    }


class ZeroHardwareSoftSensorAssimilator:
    """
    Bayesian Particle Filter (Sequential Monte Carlo) that fuses:
    - Daily mass-conserving 2-layer physics steps
    - 6-day satellite SAR surface moisture observations
    - Weekly video-frame plant turgor (root-weighted fw) & topsoil wetness bio-assays
    to estimate both topsoil (theta_1) and hidden subsoil (theta_2) without hardware sensors.
    """

    def __init__(
        self,
        n_particles: int = 80,
        z1_mm: float = 300.0,
        z2_mm: float = 500.0,
        wp: float = 0.10,
        fc: float = 0.26,
        sat: float = 0.44,
        seed: int = 42,
    ) -> None:
        self.n = n_particles
        self.z1, self.z2 = z1_mm, z2_mm
        self.wp, self.fc, self.sat = wp, fc, sat
        self.rng = np.random.default_rng(seed)
        self.ens_t1 = self.rng.uniform(0.12, 0.35, n_particles)
        self.ens_t2 = self.rng.uniform(0.14, 0.36, n_particles)
        self.ens_khp = self.rng.uniform(5.0, 70.0, n_particles)

    def _step_particle(self, t1: float, t2: float, rain: float, et0: float, khp: float) -> tuple[float, float, float, float]:
        s1, s2 = t1 * self.z1, t2 * self.z2
        s_max1, s_max2 = self.sat * self.z1, self.sat * self.z2
        s_min1, s_min2 = self.wp * self.z1, self.wp * self.z2
        infil = min(rain, max(0.0, s_max1 - s1))
        s1 += infil
        se1 = float(np.clip((s1 / self.z1 - self.fc) / (self.sat - self.fc), 0.0, 1.0))
        d12 = min(khp * (se1 ** 3.0), max(0.0, s1 - self.fc * self.z1), max(0.0, s_max2 - s2))
        s1 -= d12
        s2 += d12
        se2 = float(np.clip((s2 / self.z2 - self.fc) / (self.sat - self.fc), 0.0, 1.0))
        d2 = min(20.0 * (se2 ** 3.0), max(0.0, s2 - self.fc * self.z2))
        s2 -= d2
        fw1 = float(np.clip((s1 / self.z1 - self.wp) / (self.fc - self.wp), 0.0, 1.0))
        fw2 = float(np.clip((s2 / self.z2 - self.wp) / (self.fc - self.wp), 0.0, 1.0))
        u1 = min(max(0.0, s1 - s_min1), (0.5 * et0 + 3.5) * fw1)
        u2 = min(max(0.0, s2 - s_min2), 4.2 * fw2)
        s1 -= u1
        s2 -= u2
        return s1 / self.z1, s2 / self.z2, fw1, fw2

    def step_and_assimilate(
        self,
        rain_mm: float,
        et0_mm: float,
        sar_surface_theta1_obs: float | None = None,
        video_bio_assay: VideoFrameBioAssay | None = None,
    ) -> dict[str, float]:
        pred_fw = np.zeros(self.n, dtype=float)
        for i in range(self.n):
            r_n = max(0.0, rain_mm * self.rng.normal(1.0, 0.08))
            e_n = et0_mm * self.rng.normal(1.0, 0.06)
            t1_n, t2_n, fw1_i, fw2_i = self._step_particle(self.ens_t1[i], self.ens_t2[i], r_n, e_n, self.ens_khp[i])
            self.ens_t1[i] = float(np.clip(t1_n + self.rng.normal(0.0, 0.004), self.wp, self.sat))
            self.ens_t2[i] = float(np.clip(t2_n + self.rng.normal(0.0, 0.003), self.wp, self.sat))
            pred_fw[i] = 0.4 * fw1_i + 0.6 * fw2_i

        if sar_surface_theta1_obs is not None:
            lik = np.exp(-0.5 * ((self.ens_t1 - sar_surface_theta1_obs) / 0.028) ** 2) + 1e-12
            w = lik / np.sum(lik)
            idx = self.rng.choice(self.n, size=self.n, p=w)
            self.ens_t1, self.ens_t2, self.ens_khp = self.ens_t1[idx], self.ens_t2[idx], self.ens_khp[idx]

        if video_bio_assay is not None:
            lik = np.exp(
                -0.5 * (
                    ((self.ens_t1 - video_bio_assay.visual_topsoil_wetness_theta1) / video_bio_assay.topsoil_obs_std) ** 2
                    + ((pred_fw - video_bio_assay.visual_canopy_turgor_score) / video_bio_assay.turgor_obs_std) ** 2
                )
            ) + 1e-12
            w = lik / np.sum(lik)
            idx = self.rng.choice(self.n, size=self.n, p=w)
            self.ens_t1 = np.clip(self.ens_t1[idx] + self.rng.normal(0.0, 0.003, self.n), self.wp, self.sat)
            self.ens_t2 = np.clip(self.ens_t2[idx] + self.rng.normal(0.0, 0.003, self.n), self.wp, self.sat)
            self.ens_khp = np.clip(self.ens_khp[idx] + self.rng.normal(0.0, 1.2, self.n), 2.0, 80.0)

        return {
            "theta1_mean": float(np.mean(self.ens_t1)),
            "theta1_std": float(np.std(self.ens_t1)),
            "theta2_mean": float(np.mean(self.ens_t2)),
            "theta2_std": float(np.std(self.ens_t2)),
            "ksat_hardpan_mean": float(np.mean(self.ens_khp)),
        }