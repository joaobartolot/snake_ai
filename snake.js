// function Snake() {
//   this.x = 0;
//   this.y = 0;
//   this.xspeed = 0;
//   this.yspeed = 0;
//   this.score = 0;
//   this.tail = [];
//   this.vision = {
//     left: [-1, -1, -1],
//     right: [-1, -1, -1],
//     up: [-1, -1, -1],
//     down: [-1, -1, -1],
//   };

//   this.update = function () {
//     if (this.score === this.tail.length) {
//       for (i = 0; i < this.tail.length - 1; i++) {
//         this.tail[i] = this.tail[i + 1];
//       }
//     }

//     this.tail[this.score - 1] = createVector(this.x, this.y);

//     this.x += this.xspeed * scl;
//     this.y += this.yspeed * scl;

//     this.x = constrain(this.x, 0, width - scl);
//     this.y = constrain(this.y, 0, height - scl);
//   };

//   this.show = function () {
//     fill(255);
//     for (let i = 0; i < this.tail.length; i++) {
//       rect(this.tail[i].x, this.tail[i].y, scl, scl);
//     }
//     rect(this.x, this.y, scl, scl);
//   };

//   this.dir = function (x, y) {
//     this.xspeed = x;
//     this.yspeed = y;
//   };

//   this.eat = function (food) {
//     if (dist(food.x, food.y, this.x, this.y) < 1) {
//       this.score++;
//       return true;
//     }
//     return false;
//   };

//   this.death = function () {
//     for (var i = 0; i < this.tail.length; i++) {
//       let pos = this.tail[i];
//       let d = dist(this.x, this.y, pos.x, pos.y);

//       if (d < 1) {
//         return true;
//       }
//     }

//     return false;
//   };

//   this.look = function (food) {
//     this.vision = {
//       left: [-1, -1, dist(width - scl, this.y, this.x, this.y)],
//       right: [-1, -1, dist(0, this.y, this.x, this.y)],
//       up: [-1, -1, dist(this.x, 0, this.x, this.y)],
//       down: [-1, -1, dist(this.x, height - scl, this.x, this.y)],
//     };

//     x = floor(width / scl);
//     y = floor(height / scl);

//     for (let i = 0; i < x; i++) {
//       if (food.x === i * scl && food.y === this.y) {
//         // If there is a food in the same row of the head
//         if (this.x > i) {
//           // Checking if there is food on the LEFT
//           this.vision.left = [dist(food.x, food.y, this.x, this.y), -1, -1];
//         } else if (this.x < i) {
//           // Checking if there is food on the RIGHT
//           this.vision.right = [dist(food.x, food.y, this.x, this.y), -1, -1];
//           break;
//         }

//         for (let t = 0; t < this.tail.length; t++) {
//           if (this.tail[t].x === i * scl && this.tail[t].y === this.y) {
//             // Checking if there is a tail in the same row of the head
//             if (this.x > i) {
//               // Checking if there is food on the LEFT
//               this.vision.left = [
//                 -1,
//                 dist(this.tail[t].x, this.tail[t].y, this.x, this.y),
//                 -1,
//               ];
//             } else if (this.x < i) {
//               // Checking if there is food on the RIGHT
//               this.vision.right = [
//                 -1,
//                 dist(this.tail[t].x, this.tail[t].y, this.x, this.y),
//                 -1,
//               ];
//               break;
//             }
//           }
//         }
//       }
//     }

//     for (let i = 0; i < y; i++) {
//       if (food.y === i * scl && food.x === this.x) {
//         // If there is a food in the same row of the head
//         if (this.y > i) {
//           // Checking if there is food on the LEFT
//           this.vision.up = [dist(food.x, food.y, this.x, this.y), -1, -1];
//         } else if (this.y < i) {
//           // Checking if there is food on the RIGHT
//           this.vision.down = [dist(food.x, food.y, this.x, this.y), -1, -1];
//           break;
//         }

//         for (let t = 0; t < this.tail.length; t++) {
//           if (this.tail[t].y === i * scl && this.tail[t].x === this.x) {
//             // Checking if there is a tail in the same row of the head
//             if (this.y > i) {
//               // Checking if there is food on the LEFT
//               this.vision.up = [
//                 -1,
//                 dist(this.tail[t].x, this.tail[t].y, this.x, this.y),
//                 -1,
//               ];
//             } else if (this.y < i) {
//               // Checking if there is food on the RIGHT
//               this.vision.right = [
//                 -1,
//                 dist(this.tail[t].x, this.tail[t].y, this.x, this.y),
//                 -1,
//               ];
//               break;
//             }
//           }
//         }
//       }
//     }
//   };

//   this.getVisionData = function () {
//     let vision = [];

//     for (let i = 0; i < 3; i++) {
//       vision.push(this.vision.left[i]);
//       vision.push(this.vision.right[i]);
//       vision.push(this.vision.up[i]);
//       vision.push(this.vision.down[i]);
//     }

//     return vision;
//   };

//   this.think = function () {
//     return ai.model.predict(tf.tensor2d([this.getVisionData()]));
//   };
// }

class Snake {
  constructor() {
    this.head = new Head(createVector(width / 2, height / 2));
    this.tail = [
      new Body(createVector(this.head.pos.x - this.head.size, this.head.pos.y)),
      new Body(
        createVector(this.head.pos.x - this.head.size * 2, this.head.pos.y)
      ),
    ];
  }
  live() {
    let curr;
    this.head.draw();
    for (let i = 0; i < this.tail.length; i++) {
      curr = this.tail[i];
      if (this.head.direction) {
      }
      curr.draw();
    }
  }
  eat() {}
  checkDeath() {}
}

class Body {
  constructor(vector) {
    this.pos = vector;
    this.size = 20;
  }
  draw() {
    fill(255);
    rect(this.pos.x, this.pos.y, this.size, this.size);
  }
}

class Head extends Body {
  constructor(vector) {
    super(vector);
    this.direction = null;
  }
  move() {
    this.pos.add(this.direction);
  }
}
