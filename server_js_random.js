const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);

const mu = 0; // drift
const sigma = 0.1; // volatility
const jumpIntensity = 72; // average number of jumps per day




const jumpAmplitude = 30; // average jump size
const jumpProb = jumpIntensity / 86400; // probability of a jump in 1 second

let normalIndex = 100000;
let jumpIndex = 100000; // initial values for both indices

setInterval(() => {
  // generate a random number between 0 and 1
  const rand = Math.random();
  const r1 = randomNormal(0, 1);
  const r2 = randomNormal(0, 1);
  const r3 = randomNormal(0, 1);

  const deltaT = 1/31536000; // time step
  const drift = (mu - (sigma ** 2) / 2) * deltaT;
  const diffusion1 = sigma * Math.sqrt(deltaT) * r1;
  const diffusion2 = sigma * Math.sqrt(deltaT) * r2;
  const diffusion3 = sigma * Math.sqrt(deltaT) * r3;

  


  if (rand < jumpProb) {
    // if the random number is less than the jump probability,
    // generate a jump in the jump index
    const jumpSize = jumpAmplitude * Math.random();
    drift_corr = (-1*(jumpSize*jumpSize)*(sigma*sigma)/2 - sigma ** 2 / 2) * deltaT;

    jumpIndex *= Math.exp(drift_corr  + diffusion2 + jumpSize*diffusion3);
    normalIndex *= Math.exp(drift + diffusion1);
  } else {
    // otherwise, use the normal volatility index
    
    jumpIndex *=  Math.exp(drift + diffusion2);
    normalIndex *= Math.exp(drift + diffusion1);
  }

  io.emit('index', { normalIndex, jumpIndex });
}, 1000);


function randomNormal(mean=0, stdev=1) {
  let u = 1 - Math.random(); //Converting [0,1) to (0,1)
  let v = Math.random();
  let z = Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
  // Transform to the desired mean and standard deviation:
  return z * stdev + mean;
}

http.listen(3000, () => {
  console.log('listening on *:3000');
});
