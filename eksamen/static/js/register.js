
function init(){
    document.getElementById("searchbtn").onclick = filterContent;
    document.getElementById("edit").onclick = editContent;
    document.getElementById("back-button").onclick = mainContent;
    document.getElementById("change-apperance").onclick = changeContent;
}

window.onload = init;

function filterContent(){
    let searchtext = document.getElementById("search");
    let filter = searchtext.value.toLowerCase();
    let entry = document.getElementById("beer-content").children;
    console.log(entry[0])
    console.log(entry[0].childNodes[3].textContent)
    
    for(let i = 0; i < entry.length; i++){
        let name = entry[i].childNodes[1].textContent.toLowerCase();
        let style = entry[i].childNodes[3].textContent.toLowerCase();

        if (name.includes(filter) || style.includes(filter)){
            entry[i].style.display = "revert"
        } else{
            entry[i].style.display = "none"
        }
    }
}
function editContent(){
    document.getElementById("editform").style.display = "block"
    document.getElementById("form-elements").style.display = "none"
    document.getElementById("edit").style.display = "none"

    
}
function changeContent() {
    let element = document.getElementById("beer-content")
    let color = document.getElementById("edit-color").value;
    let size = document.getElementById("font-size").value;

    element.style.color = color;
    element.style.fontSize = size;
}
function mainContent(){
    document.getElementById("editform").style.display = "none"
    document.getElementById("form-elements").style.display = "block"
    document.getElementById("edit").style.display = "block"   
}

async function check_username(user){
    let url = "/check_username?username=" + user;
    let reply = await fetch(url);
    
    if(reply.status == 200){
        let result = await reply.text();
        document.getElementById("errmsg").innerHTML = result;

    }else{
        document.getElementById("errmsg").innerHTML = ""
    }
}
async function check_password(password){
    let url = "/check_password?password="+password;
    let reply = await fetch(url);
    if(reply.status == 200){
        let result = await reply.text();
        document.getElementById("pwmsg").innerHTML = result;
    }else{
        document.getElementById("pqmsg").innerHTML = ""
    }
}

async function update_beer(){
    let beer_name = document.getElementById("new_name").value
    let beer_style = document.getElementById("new_style").value
    let brewery_name = document.getElementById("new_bid").value
    let beerID = document.getElementById("beerID").value
    let url = "/update_beer?beer_name="+beer_name+"&beer_style="+beer_style+"&brewery_name="+brewery_name+"&beerID="+beerID;
    let reply = await fetch(url);
    if(reply.status == 200){
        
        document.location = "/beer"       
    }else{
        alert("noe gikk galt")
    }
    return false

}

async function check_login(username){
    let url = "/check_login?username=" + username;
    let reply = await fetch(url);
    
    if(reply.status == 200){
        let result = await reply.text();
        document.getElementById("loginmsg").innerHTML = result;
    }else{
        let result = await reply.text()
        document.getElementById("loginmsg").innerHTML = ""
    }
}

async function delete_beer(){
    let beerID = document.getElementById("beer-id").innerText;
    let url = "/delete_beer?beerID=" + beerID;
    let reply = await fetch(url)
    if (reply.status == 200){
        document.location = "/beer"
    }else{
        alert("feil")
    }
    return false 
}

async function check_beer_name(beer_name){
    let url = "/check_beer_name?beer_name=" + beer_name;
    let reply = await fetch(url)
    if(reply.status == 200){
        let result = await reply.text();
        document.getElementById("beermsg").innerHTML = result;
    }else{
        document.getElementById("beermsg").innerHTML = "";
    }

}