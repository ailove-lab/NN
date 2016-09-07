
//   $ clang -g -lSDL_gfx -lSDLmain -lSDL -o sdl_test sdl_test.c

#include <SDL/SDL.h>
#include <SDL/SDL_gfxPrimitives.h>

#include "cortex.h"

#define SCREEN_W  800
#define SCREEN_H  600

int main(int argc, char *argv[]) {

  SDL_Event evt; 
  int i,j;

  if (SDL_Init(SDL_INIT_VIDEO) != 0) {
    return -1;
  }

  SDL_Surface *screen = SDL_SetVideoMode(
    SCREEN_W, 
    SCREEN_H, 
    24, SDL_SWSURFACE | SDL_DOUBLEBUF);

  if (screen == NULL) {
    return -1;
  }

  cortex_init();

  while(1) {
    while(SDL_PollEvent(&evt)) {
      if(evt.type == SDL_QUIT) {
        goto finish;
      }
      if (evt.type == SDL_KEYUP && evt.key.keysym.sym == SDLK_ESCAPE) {
        goto finish;
      }
    }

    SDL_LockSurface(screen);

    SDL_FillRect(screen, NULL, 0x000080); 
    
    cortex_train();

    int scale = 5;
    fann_type xy[2];
    fann_type* res;
    unsigned int col;
    for(i=0; i<100;++i) {
      for(j=0; j<100; ++j) {
        // http://www.ferzkopp.net/Software/SDL_gfx-2.0/
        // lineColor(screen, x0, y0, x1, y1, 0xFFFFFFFF);
        xy[0] = (fann_type) i;
        xy[1] = (fann_type) j;
        res = cortex_run(xy);
        if(*res > 0) {
          col = 0xFF00004F;
        } else {
          col = 0x00FF004F;
        }
        boxColor(screen,
           i   *scale, 
           j   *scale,
          (i+1)*scale, 
          (j+1)*scale, 
          col);
      }
    }

    for(i=0; i<10; i++) {
      fann_type x = data->input[i][0];
      fann_type y = data->input[i][1];
      if(data->output[i][0] > 0) {
        col = 0xFF00007F;
      } else {
        col = 0x00FF007F;
      }
      boxColor(screen, 
        (int)  x   *scale, 
        (int)  y   *scale,
        (int) (x+1)*scale, 
        (int) (y+1)*scale, 
        col);
    }

    SDL_FreeSurface(screen);
    SDL_Flip(screen);
    // sleep(1);
  }
  
finish:
  
  cortex_destroy();
  
  SDL_FreeSurface(screen);
  SDL_Quit();

  return 0;
}
