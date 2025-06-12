import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { GenImageController } from '../gen-image/gen-image.controller';
import { GenImageService } from '../gen-image/gen-image.service';

@Module({
  imports: [],
  controllers: [AppController, GenImageController],
  providers: [AppService, GenImageService],
})
export class AppModule {}
