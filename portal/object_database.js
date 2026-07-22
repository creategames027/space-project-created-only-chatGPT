async function loadSpaceDatabase(){
 const response = await fetch('../science/database/objects.json');
 const data = await response.json();
 return data.objects;
}

async function showDatabase(){
 const objects = await loadSpaceDatabase();
 console.log('Loaded cosmic objects:', objects);
}

showDatabase();
