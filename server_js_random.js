const app = require("express")();
const http = require("http").Server(app);
const io = require("socket.io")(http);

const mu = 35; // drift
const sigma = 0.1; // volatility
const jumpIntensity = 72; // average number of jumps per day

const jumpAmplitude = 30; // average jump size
const jumpProb = jumpIntensity / 86400; // probability of a jump in 1 second

const up_prob = 0.001;

let normalIndex = 100000;
let jumpIndex = 100000;
let driftIndex = 100000;
let stepIndex = 100;
let boomIndex = 10000;

setInterval(() => {
  // generate a random number between 0 and 1
  const rand = Math.random();
  const r1 = randomNormal(0, 1);
  const r2 = randomNormal(0, 1);
  const r3 = randomNormal(0, 1);

  const deltaT = 1 / 31536000; // time step
  const drift = ((-1 * sigma ** 2) / 2) * deltaT;
  const drift2 = (mu - sigma ** 2 / 2) * deltaT;

  const diffusion1 = sigma * Math.sqrt(deltaT) * r1;
  const diffusion2 = sigma * Math.sqrt(deltaT) * r2;
  const diffusion3 = sigma * Math.sqrt(deltaT) * r3;

  step = 0.1;

  function randomNormal(mean = 0, stdev = 1) {
    let u = 1 - Math.random(); //Converting [0,1) to (0,1)
    let v = Math.random();
    let z = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    // Transform to the desired mean and standard deviation:
    return z * stdev + mean;
  }

  function normalCDF(x) {
    const t = 1 / (1 + 0.2316419 * Math.abs(x));
    const d = 0.3989423 * Math.exp((-x * x) / 2);
    const prob =
      d *
      t *
      (0.3193815 +
        t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
    if (x > 0) {
      return 1 - prob;
    }
    return prob;
  }

  const dt = deltaT;
  const sigma1 = 1;
  const mean = 1;
  const MUT = 0.00561999;
  const MDT = -5.619;

  const miu =
    sigma1 *
      Math.sqrt(2 / Math.PI) *
      Math.exp((-1 * mean ** 2) / (2 * sigma1 ** 2)) +
    mean * (1 - 2 * normalCDF((-1 * mean) / sigma1));

  const random = randomNormal(mean, sigma1);

  if (Math.random() > up_prob) {
    boomIndex *= Math.exp(MUT * (Math.abs(random) / miu) * Math.sqrt(dt));
  } else {
    boomIndex *= Math.exp(MDT * (Math.abs(random) / miu) * Math.sqrt(dt));
  }

  //stepping up/down
  if (rand >= 0.5) {
    stepIndex += step;
  } else {
    stepIndex -= step;
  }

  ///jumping occurance
  if (rand < jumpProb) {
    // if the random number is less than the jump probability,
    // generate a jump in the jump index
    const jumpSize = jumpAmplitude * Math.random();
    drift_corr =
      ((-1 * (jumpSize * jumpSize) * (sigma * sigma)) / 2 - sigma ** 2 / 2) *
      deltaT;

    jumpIndex *= Math.exp(drift_corr + diffusion2 + jumpSize * diffusion3);
  } else {
    // otherwise, use the normal volatility index
    jumpIndex *= Math.exp(drift + diffusion2);
  }

  normalIndex *= Math.exp(drift + diffusion1);
  driftIndex *= Math.exp(drift2 + diffusion1);

  io.emit("index", {
    normalIndex,
    jumpIndex,
    driftIndex,
    stepIndex,
    boomIndex,
  });
}, 1000);

http.listen(3000, () => {
  console.log("listening on *:3000");
});
