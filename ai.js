function Ai() {
  this.model = tf.sequential();

  this.setup = function () {
    this.model.add(tf.layers.inputLayer({ inputShape: [12] }));
    this.model.add(
      tf.layers.dense({
        units: 16,
        activation: "relu",
      })
    );

    this.model.add(
      tf.layers.dense({
        units: 16,
        activation: "relu",
      })
    );
    this.model.add(
      tf.layers.dense({
        units: 4,
        activation: "sigmoid",
      })
    );

    // this.model.summary();
  };
}
