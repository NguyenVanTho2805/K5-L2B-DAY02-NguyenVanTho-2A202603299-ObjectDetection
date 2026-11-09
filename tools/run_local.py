"""Chay lai notebook day2_annotation_to_yolo.ipynb tren may (khong clone).

Giong notebook: yolo26n.pt, epochs=50, imgsz=640, batch=-1, seed=20260909,
val tren 10 anh eval, predict conf=0.25, zip outputs. data.yaml goc khong bi sua:
ban co path tuyet doi duoc ghi vao outputs/data_local.yaml.
"""
import json
import platform
import shutil
import sys
from pathlib import Path

import torch
import ultralytics
import yaml
from ultralytics import YOLO


def main():
    LAB_ROOT = Path(sys.argv[1]).resolve()
    TRAIN_IMAGES = LAB_ROOT / "dataset/images/train"
    TRAIN_LABELS = LAB_ROOT / "dataset/labels/train"
    EVAL_IMAGES = LAB_ROOT / "dataset/images/eval"
    EVAL_LABELS = LAB_ROOT / "dataset/labels/eval"
    OUT = LAB_ROOT / "outputs"
    RUNS = OUT / "yolo26_runs"
    DEVICE = 0 if torch.cuda.is_available() else "cpu"
    OUT.mkdir(exist_ok=True)

    cfg = yaml.safe_load((LAB_ROOT / "data.yaml").read_text(encoding="utf-8"))
    cfg["path"] = str((LAB_ROOT / "dataset").resolve())
    DATA_YAML = OUT / "data_local.yaml"
    DATA_YAML.write_text(yaml.dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8")

    print("python", platform.python_version(), "| torch", torch.__version__,
          "| ultralytics", ultralytics.__version__, "| device", DEVICE, platform.processor(), flush=True)

    def stems(d):
        return {p.stem for ext in ("*.jpg", "*.jpeg", "*.png") for p in d.glob(ext)}

    train_images, eval_images = stems(TRAIN_IMAGES), stems(EVAL_IMAGES)
    assert len(train_images) == 50 and train_images == {p.stem for p in TRAIN_LABELS.glob("*.txt")}
    assert len(eval_images) == 10 and eval_images == {p.stem for p in EVAL_LABELS.glob("*.txt")}
    print("OK: 50 train + 10 eval", flush=True)

    model = YOLO("yolo26n.pt")
    model.train(data=str(DATA_YAML), epochs=50, imgsz=640, batch=-1, device=DEVICE,
                project=str(RUNS), name="vehicle_annotation", exist_ok=True,
                seed=20260909, plots=True, workers=0)
    BEST = Path(model.trainer.best)
    print("best checkpoint:", BEST, flush=True)

    best_model = YOLO(str(BEST))
    m = best_model.val(data=str(DATA_YAML), split="val", device=DEVICE, plots=True,
                       project=str(RUNS), name="vehicle_eval", exist_ok=True, workers=0)
    summary = {
        "precision": float(m.box.mp), "recall": float(m.box.mr),
        "map50": float(m.box.map50), "map50_95": float(m.box.map),
        "eval_images": len(eval_images), "checkpoint": str(BEST),
        "per_class": {m.names[c]: {"precision": float(p), "recall": float(r), "map50": float(a50), "map50_95": float(a)}
                      for c, p, r, a50, a in zip(m.box.ap_class_index, m.box.p, m.box.r, m.box.ap50, m.box.ap)},
        "runtime": f"local {DEVICE} | torch {torch.__version__} | ultralytics {ultralytics.__version__}",
    }
    (OUT / "model_eval_metrics.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)

    res = best_model.predict(source=str(EVAL_IMAGES), conf=0.25, device=DEVICE, save=True,
                             project=str(OUT / "eval_predictions"), name="visuals", exist_ok=True)
    print("predictions saved to:", res[0].save_dir, flush=True)
    stage = OUT / "_zip" / "day2_colab_outputs"
    if stage.parent.exists():
        shutil.rmtree(stage.parent)
    for name in ("eval_predictions", "yolo26_runs", "model_eval_metrics.json"):
        src = OUT / name
        (shutil.copytree if src.is_dir() else shutil.copy2)(src, stage / name if src.is_dir() else stage.mkdir(parents=True, exist_ok=True) or stage / name)
    print("Da tao:", shutil.make_archive(str(OUT / "day2_colab_outputs"), "zip", stage.parent), flush=True)
    shutil.rmtree(stage.parent)


if __name__ == "__main__":
    main()
