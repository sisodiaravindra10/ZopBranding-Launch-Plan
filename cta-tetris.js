// CTA-TETRIS · self-playing Tetris loop in the .final section's right column.
// Mounts onto <canvas id="tet-canvas">. Resizes to its container. No-op if
// the canvas isn't present (so it's safe to load on pages without the CTA).
(function(){
  var canvas = document.getElementById('tet-canvas');
  if(!canvas) return;
  var ctx = canvas.getContext('2d');
  var SIZE = 44;
  var COLS = 1, ROWS = 1;
  var grid = [];
  var active = null;
  var totalLines = 0;

  function resetGrid(){
    grid = Array.from({length:ROWS}, function(){ return Array(COLS).fill(0); });
  }
  function resize(){
    var dpr = window.devicePixelRatio || 1;
    var w = canvas.clientWidth;
    var h = canvas.clientHeight;
    if(w<=0 || h<=0) return;
    COLS = Math.max(3, Math.floor(w / SIZE));
    ROWS = Math.max(6, Math.floor(h / SIZE));
    canvas.width  = COLS * SIZE * dpr;
    canvas.height = ROWS * SIZE * dpr;
    ctx.setTransform(dpr,0,0,dpr,0,0);
    resetGrid();
    active = null;
  }

  // Brand palette · 3 brand colors only, no ink/black accents
  var COLORS = {
    1:'#2A4494', // ZopDev blue
    2:'#F58549', // ZopDev orange
    3:'#7FB236'  // ZopDev green
  };

  // Tetrominoes, 4x4 matrices, 1=filled
  var SHAPES = [
    // I
    [[[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],
     [[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]]],
    // O
    [[[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]],
    // T
    [[[0,0,0,0],[1,1,1,0],[0,1,0,0],[0,0,0,0]],
     [[0,1,0,0],[1,1,0,0],[0,1,0,0],[0,0,0,0]],
     [[0,1,0,0],[1,1,1,0],[0,0,0,0],[0,0,0,0]],
     [[0,1,0,0],[0,1,1,0],[0,1,0,0],[0,0,0,0]]],
    // L
    [[[1,0,0,0],[1,1,1,0],[0,0,0,0],[0,0,0,0]],
     [[1,1,0,0],[1,0,0,0],[1,0,0,0],[0,0,0,0]],
     [[1,1,1,0],[0,0,1,0],[0,0,0,0],[0,0,0,0]],
     [[0,1,0,0],[0,1,0,0],[1,1,0,0],[0,0,0,0]]],
    // J
    [[[0,0,1,0],[1,1,1,0],[0,0,0,0],[0,0,0,0]],
     [[1,0,0,0],[1,0,0,0],[1,1,0,0],[0,0,0,0]],
     [[1,1,1,0],[1,0,0,0],[0,0,0,0],[0,0,0,0]],
     [[1,1,0,0],[0,1,0,0],[0,1,0,0],[0,0,0,0]]],
    // S
    [[[0,1,1,0],[1,1,0,0],[0,0,0,0],[0,0,0,0]],
     [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,0,0,0]]],
    // Z
    [[[1,1,0,0],[0,1,1,0],[0,0,0,0],[0,0,0,0]],
     [[0,1,0,0],[1,1,0,0],[1,0,0,0],[0,0,0,0]]]
  ];

  function pick(arr){ return arr[Math.floor(Math.random()*arr.length)]; }
  function collides(shape, x, y){
    for(var r=0;r<4;r++) for(var c=0;c<4;c++){
      if(!shape[r][c]) continue;
      var gx=x+c, gy=y+r;
      if(gx<0||gx>=COLS||gy>=ROWS) return true;
      if(gy>=0 && grid[gy][gx]) return true;
    }
    return false;
  }
  function merge(shape, x, y, color){
    for(var r=0;r<4;r++) for(var c=0;c<4;c++){
      if(shape[r][c] && y+r>=0) grid[y+r][x+c] = color;
    }
  }
  function clearLines(){
    var cleared = 0;
    for(var r=ROWS-1; r>=0; r--){
      if(grid[r].every(function(v){return v!==0;})){
        grid.splice(r,1);
        grid.unshift(Array(COLS).fill(0));
        cleared++; r++;
      }
    }
    return cleared;
  }
  function draw(active){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    for(var r=0;r<ROWS;r++) for(var c=0;c<COLS;c++){
      if(grid[r][c]){
        ctx.fillStyle = COLORS[grid[r][c]];
        ctx.fillRect(c*SIZE, r*SIZE, SIZE, SIZE);
      }
    }
    if(active){
      ctx.fillStyle = COLORS[active.color];
      for(var rr=0;rr<4;rr++) for(var cc=0;cc<4;cc++){
        if(active.shape[rr][cc]){
          var gx=active.x+cc, gy=active.y+rr;
          if(gy>=0) ctx.fillRect(gx*SIZE, gy*SIZE, SIZE, SIZE);
        }
      }
    }
  }
  function spawn(){
    var rotations = pick(SHAPES);
    var shape = pick(rotations);
    var bestX = 0, bestY = -2;
    for(var t=0;t<5;t++){
      var x = Math.floor(Math.random()*Math.max(1, COLS-2));
      var y = -2;
      while(!collides(shape, x, y+1)) y++;
      if(y>bestY){ bestY = y; bestX = x; }
    }
    var color = 1 + Math.floor(Math.random()*3);
    active = { shape:shape, x:bestX, y:-2, color:color };
  }
  function tick(){
    if(!active){ spawn(); }
    if(!collides(active.shape, active.x, active.y+1)){
      active.y++;
    } else {
      merge(active.shape, active.x, active.y, active.color);
      var cleared = clearLines();
      if(cleared) totalLines += cleared;
      if(grid[1] && grid[1].some(function(v){return v!==0;})){
        grid = Array.from({length:ROWS}, function(){ return Array(COLS).fill(0); });
      }
      active = null;
    }
    draw(active);
  }

  resize();
  window.addEventListener('resize', function(){
    clearTimeout(window.__tetResize);
    window.__tetResize = setTimeout(resize, 120);
  });
  draw(null);
  setInterval(tick, 240);
})();
