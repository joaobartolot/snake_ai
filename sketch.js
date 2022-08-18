let scl = 20;

let player;
let snake;
let food;
let ai;

function setup() {
  createCanvas(
    floor(window.innerWidth / scl) * scl,
    floor(window.innerHeight / scl) * scl
  );

  frameRate(15);
  div = createDiv(`
    Score: 0<br>
    Record: 0
  `).addClass("score");
  gameOver = createDiv(`
    <h1>Game Over</h1>
    <p>Press "F" to play again</p>
  `).addClass("game-over");

  player = new Player();
  snake = new Snake();
  food = new Food();

  ai = new Ai();

  ai.setup();

  // snake.think();
}

function draw() {
  background(0);

  if (snake.eat(food)) {
    food.updateLocation();
    player.newRecord(snake.score);
    div.html(`
      Score: ${snake.score}<br>
      Record: ${player.record}
    `);
  }
  // if (snake.death()) {
  //   gameOver.style("display: flex");
  // } else {
  snake.live();
  // snake.update();
  // snake.show();

  // snake.look(food);

  food.show();
  // }
}

function keyPressed() {
  if (keyCode === UP_ARROW) {
    snake.dir(0, -1);
  } else if (keyCode === DOWN_ARROW) {
    snake.dir(0, 1);
  } else if (keyCode === RIGHT_ARROW) {
    snake.dir(1, 0);
  } else if (keyCode === LEFT_ARROW) {
    snake.dir(-1, 0);
  }

  if (keyCode === 70) {
    snake = new Snake();
    food = new Food();

    snake.score = 0;

    gameOver.hide();

    if (player.record != 0) {
      div.html(`
        Score: 0<br>
        Record: ${player.record}
      `);
    } else {
      div.html(`
        Score: 0<br>
        Record: 0
      `);
    }
  }
}
