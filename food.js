class Food {
  constructor() {
    this.shize = 20;
    this.updateLocation();
  }

  updateLocation() {
    let cols = floor(width / this.size);
    let rows = floor(height / this.size);

    this.pos = createVector(random(rows) * this.size, random(cols) * this.size);
  }

  show() {
    fill(0, 220, 0);
    rect(this.pos.x, this.pos.y, this.size, this.size);
  }
}
