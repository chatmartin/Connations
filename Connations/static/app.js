const grid = document.getElementById("grid");
const newBoardButton = document.getElementById("new");
const submitButton = document.getElementById("submit");
const deselButton = document.getElementById("deselect");
const shufButton = document.getElementById("shuffle");
const banners = document.getElementById('banners');
const message = document.getElementById('message');
const shareButton = document.getElementById('share');
const infoButton = document.getElementById("infoButton");
const infoModal = document.getElementById("infoModal");
const closeModal = document.getElementById("closeModal");
const tabButtons = document.querySelectorAll(".tab-button");
const tabContents = document.querySelectorAll(".tab-content");

let selected = [];
let lockedTiles = [];
let history = [];
let gameOver = false;

let triesLeft = 4;
const triesDisplay = document.createElement('p');
triesDisplay.id = 'attempts';
triesDisplay.innerText = "Strikes left: " + "🌍".repeat(triesLeft);
document.body.insertBefore(triesDisplay,message);

var countries = [
    'Albania', 'Türkiye', 'Liberia', 'Pakistan',
    'United Kingdom', 'France', 'India', 'Serbia',
    'China', 'North Korea', 'United States of America', 'Argentina',
    'Brazil', 'Poland', 'Canada', 'Finland'
]
const groups = [
    {countries:["Albania",'Türkiye','Liberia','Pakistan'], reason:"GOAT", color: "#FFD700"},
    {countries:['United Kingdom', 'France', 'India', 'Serbia'], reason:"LOSER", color: "#FF6347"},
    {countries:['China', 'North Korea', 'United States of America', 'Argentina'], reason:"GLORIOUS LEADER", color: "#1E90FF"},
    {countries:['Brazil', 'Poland', 'Canada', 'Finland'], reason:"CURSED", color: "#32CD32"}
]

infoButton.addEventListener("click", () => {
    infoModal.style.display = "flex";
  });
  
  closeModal.addEventListener("click", () => {
    infoModal.style.display = "none";
  });
  
  infoModal.addEventListener("click", (e) => {
    if (e.target === infoModal) {
      infoModal.style.display = "none";
    }
  });
  
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      tabButtons.forEach(b => b.classList.remove("active"));
      tabContents.forEach(c => c.classList.remove("active"));
  
      btn.classList.add("active");
      document.getElementById(btn.dataset.tab).classList.add("active");
    });
  });

async function initGame(){
    const res = await fetch("/init");
    const data = await res.json();
    countries = data.tiles
    renderGrid();
    triesLeft = data.tries;
}

function shuffleArray(array){
    let currInd = array.length-1;
    let randInd;
    while(currInd != 0){
        randInd = Math.floor(Math.random()*(currInd+1));
        temp = array[currInd];
        array[currInd]=array[randInd];
        array[randInd]=temp;
        currInd--;
    }
}

function tileClick(div,country){
    if(div.classList.contains("selected")){
        div.classList.remove("selected")
        selected = selected.filter(c => c !== country);
    }
    else{
        if(selected.length < 4){
            div.classList.add("selected");
            selected.push(country);
        }
    }
    submitButton.disabled = selected.length !==4;
}

async function submitGuess(){
    const res = await fetch("/check",{
        method:"POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({guess:selected})
    });
    const result = await res.json();
    const tiles = document.querySelectorAll(".grid-item");
    tiles.forEach(tile=>{
        if(selected.includes(tile.innerText)){
            tile.classList.add("jump");
            setTimeout(()=>tile.classList.remove("jump"),300);
        }
    });
    if(result.correct===2){
        const bannerDiv = document.createElement("div");
        bannerDiv.classList.add("banner");
        bannerDiv.style.background = result.color;
        const title = document.createElement("span");
        title.classList.add("banner-title");
        title.innerText = result.reason;
        bannerDiv.appendChild(title);

        const tileDiv = document.createElement("div");
        tileDiv.classList.add("banner-tiles");

        selected.forEach(country => {
            const tile = document.createElement("span");
            tile.classList.add("tile");
            tile.innerText = country;
            tileDiv.appendChild(tile);
            lockedTiles.push(country);
        });

        message.innerText = "";

        bannerDiv.appendChild(tileDiv);
        banners.appendChild(bannerDiv);

        renderGrid();
    }
    else {
        countries.forEach(country =>{
            if (selected.includes(country)){
                grid.classList.add('shake');
                setTimeout(() => grid.classList.remove("shake"),300);
            }
        });
        triesLeft = result.tries;
        triesDisplay.innerText = "Strikes left: " + "🌍".repeat(triesLeft);
        if(result.correct === 1){
            message.innerText = "One away...";
        }
        else{
            message.innerText = "";
        }
    }
    colors = result.result;
    if(!gameOver){
        history_block = [];
        colors.forEach(color =>{
            if(color === "B")
                history_block.push("🟦");
            if(color === "G")
                history_block.push("🟩");
            if(color === "Y")
                history_block.push("🟨");
            if(color === "R")
                history_block.push("🟥");
        });
        history.push(history_block);
    }
}

/*function submit(){
    const guessSet = new Set(selected);
    let correctGroup = null;
  
    for (const group of groups) {
      const groupSet = new Set(group.countries);
      if (groupSet.size === guessSet.size && [...groupSet].every(country => guessSet.has(country))) {
        correctGroup = group;
        break;
      }
    }
  
    if (correctGroup) {
        const bannerDiv = document.createElement("div");
        bannerDiv.classList.add("banner");
        bannerDiv.style.background = correctGroup.color;
        const title = document.createElement("span");
        title.innerText = correctGroup.reason + ": "
        bannerDiv.appendChild(title);

        correctGroup.countries.forEach(country => {
            const tile = document.createElement("span");
            tile.classList.add("tile");
            tile.innerText = country;
            bannerDiv.appendChild(tile);
            lockedTiles.push(country);
        });

        banners.appendChild(bannerDiv);

        renderGrid();
    } 
    else {
        countries.forEach(country =>{
            if (selected.includes(country)){
                grid.classList.add('shake');
                setTimeout(() => grid.classList.remove("shake"),300);
            }
        });
        triesLeft--;
        triesDisplay.innerText = "Strikes left: " + "🌍".repeat(triesLeft);;
    }
}*/

function renderGrid(){
    grid.innerHTML = "";
    selected = [];
    submitButton.disabled = true;

    countries.forEach(country => {
        if(lockedTiles.includes(country)) return;
        const div = document.createElement('div');
        div.classList.add("grid-item");
        div.innerText = country;
        div.addEventListener("click", () => {
            tileClick(div,country);
        });

        grid.appendChild(div);
    });
}

async function gameLoss(){
    gameOver = true;
    selected = [];
    document.querySelectorAll(".grid-item.selected").forEach(div => div.classList.remove("selected"));
    grid.classList.add("disabled");
    renderGrid();
    submitButton.disabled = true;
    const tiles = document.querySelectorAll(".grid-item");
    const res = await fetch("/loss");
    const data = await res.json();
    for(const group of data.groups) {
        if(group.countries.every(country => lockedTiles.includes(country))) continue;
        selected = [...group.countries]
        await new Promise(r=>setTimeout(r,800));
        await submitGuess();
    };
    message.innerText = "Game over. Better luck next time."
    grid.classList.remove("disabled");
    message.style.color = "black";
    selected = [];
    document.querySelectorAll(".grid-item.selected").forEach(div => div.classList.remove("selected"));
}

submitButton.addEventListener("click", async () => {
    await submitGuess();
    if(triesLeft === 0){
        await gameLoss();
        shareButton.style.display = "inline-block";
    }
    else if(lockedTiles.length === countries.length){
        message.innerText = "Congratulations! You found all the connections."
        shareButton.style.display = "inline-block";
    }
});

deselButton.addEventListener("click", () => {
    selected = [];
    document.querySelectorAll(".grid-item.selected").forEach(div => div.classList.remove("selected"));
    renderGrid();
    submitButton.disabled = true;
});

shufButton.addEventListener("click", () =>{
    const remaining = countries.filter(country => !lockedTiles.includes(country))
    shuffleArray(remaining);
    countries.length = 0
    countries.push(...lockedTiles,...remaining);
    renderGrid();
});

newBoardButton.addEventListener("click", async () => {
    await fetch("/new")
    gameOver = false;
    lockedTiles = [];
    selected = [];
    history = [];
    shareButton.style.display = "none";
    banners.innerHTML = "";
    message.innerText = "";
    await initGame();
    triesDisplay.innerText = "Strikes left: " + "🌍".repeat(triesLeft);
});

shareButton.addEventListener("click", () => {
    text = ''
    history.forEach(history_block => {
        history_block.forEach(color =>{
            text += color;
        });
        text += '\n';
    });
    navigator.clipboard.writeText(text).then(()=>{
        alert("Results copied to clipboard");
    }).catch(err => {
        console.error("Clipboard copy failed: ", err);
    });
});

shuffleArray(countries)
shuffleArray(countries)
shuffleArray(countries)
initGame();