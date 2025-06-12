import sys
import os
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import torch
import hashlib

def generate_cache_key(prompt):
    return hashlib.md5(prompt.encode()).hexdigest()

def should_regenerate(output_path, force=False):
    if force:
        return True
    return not os.path.exists(output_path)

if len(sys.argv) < 3:
    print("Error: Missing required arguments. Usage: python generate.py <prompt> <output_path> [--force]")
    sys.exit(1)

prompt = sys.argv[1]
output_path = sys.argv[2]
force_regenerate = len(sys.argv) > 3 and sys.argv[3] == "--force"

if not prompt or not prompt.strip():
    print("Error: Prompt is empty")
    sys.exit(1)

if not should_regenerate(output_path, force_regenerate):
    print(f"File {output_path} already exists, skipping generation. Use --force to regenerate.")
    sys.exit(0)

output_dir = os.path.dirname(output_path)
if output_dir:
    os.makedirs(output_dir, exist_ok=True)

negative_prompt = "blurry, low quality, worst quality, low resolution, pixelated, jpeg artifacts, bad anatomy, bad hands, missing fingers, extra fingers, mutated hands, deformed, disfigured, ugly, poorly drawn, amateur, sketch, rough, grainy, distorted, warped"

try:
    print("Loading SDXL model for highest quality...")
    
    pipe = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        use_safetensors=True,
        variant="fp16" if torch.cuda.is_available() else None
    )
    
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = pipe.to(device)
    
    if torch.cuda.is_available():
        pipe.enable_attention_slicing()
        pipe.enable_model_cpu_offload()
    
    print(f"Model loaded on {device}")
    print("Generating high-quality image...")
    
    enhanced_prompt = f"{prompt}, masterpiece, best quality, ultra detailed, 8k, photorealistic, professional photography, sharp focus, vibrant colors, perfect lighting"
    
    result = pipe(
        prompt=enhanced_prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=50,
        guidance_scale=8.0,
        width=1024,
        height=1024,
        generator=torch.Generator(device=device).manual_seed(42)
    )
    
    if result is None or not hasattr(result, 'images') or result.images is None or len(result.images) == 0:
        print("Error: No images generated")
        sys.exit(1)
    
    image = result.images[0]
    
    image.save(output_path, quality=95, optimize=True)
    
    print(f"Generated high-quality image: {output_path}")
    print(f"Resolution: 1024x1024")
    print(f"Enhanced prompt used: {enhanced_prompt}")
    
except Exception as e:
    print(f"Error during generation: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)