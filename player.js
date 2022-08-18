function Player() {
  this.record = 0;

  this.newRecord = function (score) {
    if (score > this.record) {
      this.record = score;
    }
  };
}
