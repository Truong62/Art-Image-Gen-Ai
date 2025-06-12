import { Controller, Post, Body } from '@nestjs/common';
import { GenImageService } from './gen-image.service';

@Controller('genImage')
export class GenImageController {
  constructor(private readonly service: GenImageService) {}

  @Post()
  async generate(@Body() body: { prompt: string }) {
    const file = await this.service.generateImage(body.prompt);
    return { imageUrl: `/images/${file}` };
  }
}
