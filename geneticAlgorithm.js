function GeneticAlgorithm(
  initPopulation,
  generation,
  mutationRate,
  crossOverRate
) {
  this.initPopulation = initPopulation;
  this.generation = generation;
  this.mutationRate = mutationRate;
  this.crossOverRate = crossOverRate;
  this.population = [];
  this.currentGeneration = 0;

  this.createPopulation = function () {
    let model;
    for (let i = 0; i < this.initPopulation; i++) {
      model = new Ai();
      model.setup();
      this.population.push(model);
    }
  };

  this.createGeneration;
}
