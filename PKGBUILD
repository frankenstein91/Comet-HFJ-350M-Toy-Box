# Maintainer: DO3EET <do3eet@example.com>
pkgname=python-toybox-calc
_pkgname=toybox-calc
pkgver=0.0.1_preclt2026
pkgrel=1
pkgdesc="Comet HFJ-350M Toy Box configuration calculator"
arch=('any')
url="https://github.com/frankenstein91/Comet-HFJ-350M-Toy-Box"
license=('MIT')
depends=('python')
makedepends=('python-build' 'python-installer' 'python-setuptools' 'python-wheel')
source=("${_pkgname}-${pkgver}.tar.gz::https://github.com/frankenstein91/Comet-HFJ-350M-Toy-Box/archive/refs/tags/v${pkgver}.tar.gz")
sha256sums=('SKIP') # You will need to update this after creating a tag/release

build() {
    cd "${_pkgname}-${pkgver}"
    python -m build --wheel --no-isolation
}

package() {
    cd "${_pkgname}-${pkgver}"
    python -m installer --destdir="$pkgdir" dist/*.whl
    
    # Install license
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
    # Install disclaimer as well
    install -Dm644 DISCLAIMER.md "$pkgdir/usr/share/doc/$pkgname/DISCLAIMER.md"
}
