const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Function to draw images with transparency
function drawBase64Image(base64, alpha = 1.0) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = function() {
      ctx.globalAlpha = alpha;
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      ctx.globalAlpha = 1.0; // Reset alpha
      resolve();
    };
    img.onerror = reject;
    img.src = base64;
  });
}

  // Function to draw points
function drawPoints(points, colors, size) {;
    points.forEach((point, index) => {
	  color = colors[index];
      ctx.fillStyle = `rgba(${color[0] * 255}, ${color[1] * 255}, ${color[2] * 255}, ${color[3]})`;
      ctx.beginPath();
      ctx.arc(point.x, point.y, size, 0, 2 * Math.PI);
      ctx.fill();
    });
  }

function drawLinks(pose) {
  if (pose && pose.links && pose.links.u && pose.links.v) {
    pose.links.u.forEach((start, index) => {
      const end = pose.links.v[index];
      const color = pose.links.c[index];
      ctx.strokeStyle = `rgba(${color[0] * 255}, ${color[1] * 255}, ${color[2] * 255}, 1)`;
	  console.log(ctx.strokeStyle);
      ctx.beginPath();
      ctx.moveTo(start[0], end[0]);
      ctx.lineTo(start[1], end[1]);
      ctx.stroke();
    });
  }
}

async function render(data, i) {
  //await drawBase64Image(data.vid, 1);
  //await drawBase64Image(data.aligned, 0.5);

  const pcPoints = data.pc.px.map((x, i) => ({x: x, y: data.pc.py[i]}));
  drawPoints(pcPoints, data.pc.c, 5);

  const kptsPoints = data.pose.kpts.px.map((x, i) => ({x: x, y: data.pose.kpts.py[i]}));
  drawPoints(kptsPoints, data.pose.kpts.c, 2.5);
  drawLinks(data.pose);
}

socket.on('data', function(data) {
  data = data["data"];
  i = data["pk"];

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  render(data, i);
});
