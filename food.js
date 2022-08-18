function Food() {
  this.x = 0;
  this.y = 0;

  this.updateLocation = function () {
    let cols = floor(width / scl);
    let rows = floor(height / scl);
    this.x = floor(random(cols)) * scl;
    this.y = floor(random(rows)) * scl;
  };

  this.show = function () {
    fill(0, 220, 0);
    rect(this.x, this.y, scl, scl);
  };

  this.updateLocation();
}
