import { Injectable } from '@nestjs/common';
import { spawn } from 'child_process';
import * as fs from 'fs';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class GenImageService {
  async generateImage(prompt: string): Promise<string> {
    const filename = `${uuidv4()}.png`;
    const outputPath = `./images/${filename}`;

    await new Promise((resolve, reject) => {
      const process = spawn('python3', [
        'src/ai-engine/generate.py',
        prompt,
        outputPath,
      ]);

      process.stdout.on('data', (data) => console.log(`stdout: ${data}`));
      process.stderr.on('data', (data) => console.error(`stderr: ${data}`));
      process.on('close', (code) => {
        if (code === 0) resolve(true);
        // eslint-disable-next-line @typescript-eslint/prefer-promise-reject-errors
        else reject(`Process exited with code ${code}`);
      });
    });

    if (!fs.existsSync(outputPath)) {
      throw new Error('Image not created');
    }

    return filename;
  }
}
