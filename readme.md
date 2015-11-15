# WebHDR Utilities

This repository contains a utility for encoding HDR images for WebGL display as
well as an example viewer. The encoding utility works with either Python 2 or
Python 3 and requires [NumPy](http://www.numpy.org/) and
[ImageIO](https://imageio.github.io/). The encoder was tested using OpenEXR
input images. For more information, see
[this blog post](https://mpetroff.net/2015/11/bandwidth-efficient-hdr-webgl-textures/).

The method implemented is based on:
Francesco Banterle and Roberto Scopigno. BoostHDR: a novel backward-
compatible method for HDR images. 2012. DOI: [10.1117/12.931504](http://dx.doi.org/10.1117/12.931504). URL:
[http://vcg.isti.cnr.it/Publications/2012/BS12/spie\_2012\_compression\_hdr.pdf](http://vcg.isti.cnr.it/Publications/2012/BS12/spie\_2012\_compression\_hdr.pdf).

## License

The contents of this repository are released into the public domain using the
[CC0 1.0 Public Domain Dedication](https://creativecommons.org/publicdomain/zero/1.0/).

## Credits

* [Matthew Petroff](https://mpetroff.net/)
