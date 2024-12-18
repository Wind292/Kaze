const multer = require('multer');
const express = require('express');
const path = require('path');
const fs = require('fs');
const cors = require('cors'); // Import CORS middleware
const app = express();

let compque = []
// {
//   url: "",
//   compressionquality: "med"
// }


function auth(username, password) {
  const filePath = path.join(__dirname, `./passwords.json`);
  fs.readFile(filePath, 'utf8', (err, data) => {
    data = JSON.parse(data)
    if (err) {
      console.error("Error reading file:", err); // Log the error
      console.log('ERROR READING PASSWORDS FILE')
      return false
    }
    if (!(data.users.some(user => user[username] === password))) {
      return false;
    }
    return true;
  })
}

// Enable CORS for all routes
app.use(cors());

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

const upload = multer({ dest: './public/' });





// Route for the homepage
app.get('/', (req, res) => {
  res.send('Stop doing that');
});


app.get('/startnc', async (req, res) => { // send a url
  if (compque.length === 0){
    res.status(204).json({ message: "No tasks" });
    return
  }

  let x  = compque.shift();
  res.status(200).json({ message: x });
});

app.post('/finishnc', upload.single('file'), (req, res) => {
  if (!req.file) {
      return res.status(400).send('No file uploaded.');
  }


  console.log('File received:', req.file);

  console.log(req.body.path)
  fs.rename(req.file.path, "./public/"+req.body.path[0]+'/'+req.body.path[1], (err) => {
    if (err) {
        console.error('Error renaming file:', err);
        return res.status(500).send('Failed to rename uploaded file.');
    }
    
    console.log('File renamed successfully');
  });


  res.send(`File ${req.file.originalname} uploaded successfully.`);
});



// Dynamic route for fetching user info from JSON files
app.get('/usrinfo/:username', (req, res) => {
  const username = req.params.username;
  const filePath = path.join(__dirname, `./public/${username}/info.json`);

  // Check if the file exists
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error("Error reading file:", err); // Log the error
      if (err.code === 'ENOENT') {
        return res.status(404).send({ error: 'User not found' });
      }
      return res.status(500).send({ error: 'Server error' });
    }
    res.json(JSON.parse(data));
  });
});

app.get('/passwordcheck', async (req, res) => {
  const { password, username } = req.query;


  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // await sleep(400)

  const filePath = path.join(__dirname, `./passwords.json`);
  fs.readFile(filePath, 'utf8', (err, data) => {

    

    data = JSON.parse(data)
    
    if (err) {
      console.error("Error reading file:", err); // Log the error
      if (err.code === 'ENOENT') {
        console.log('other')
        res.send("Server Error")
        return
      }
      console.log('other')
      res.send("Server Error")
      return
    }


    if (!(data.users.some(user => user[username] === password))) {
      console.log('user no find');
      res.send("Username or Password Incorrect");
      return;
    }

    res.send("Ok");
    return;
  });
})

app.get('/createaccount', async (req, res) => {
    const { bio, id: idRaw, disname, password } = req.query;

    id = idRaw.toLowerCase()

    // Validate username
    if (!validUsername(id)) {
        return res.send('Not a valid User ID, tip: User IDs can only be numbers, lowercase letters, and _');
    }

    try {
        const userListPath = path.join(__dirname, './userlist.json');
        const userListData = await fs.promises.readFile(userListPath, 'utf8');
        const jsonData = JSON.parse(userListData);

        // Check if username is already taken
        if (jsonData.users.includes(id)) {
            return res.send('Username already taken');
        }

        // Add user to userlist.json
        jsonData.users.push(id);
        const updatedJson = JSON.stringify(jsonData, null, 2);
        await fs.promises.writeFile(userListPath, updatedJson);

        // Create user directory and info.json file
        const userDir = path.join(__dirname, 'public', id);
        await fs.promises.mkdir(userDir, { recursive: false });

        const userInfo = {
            userid: id,
            display_name: disname,
            bio: bio,
            videos: []
        };
        const userInfoPath = path.join(userDir, 'info.json');
        await fs.promises.writeFile(userInfoPath, JSON.stringify(userInfo, null, 2));

        const passwordsPath = path.join(__dirname, './passwords.json');
        const passwordsData = await fs.promises.readFile(passwordsPath, 'utf8');
        const passworsJsonData = JSON.parse(passwordsData);

        passworsJsonData.users.push({[id]: password});
        const updatedPasswordsJson = JSON.stringify(passworsJsonData, null, 2);
        await fs.promises.writeFile(passwordsPath, updatedPasswordsJson);

        console.log('New user successfully added and folder created');
        res.send('Ok');

    } catch (err) {
        console.error('Error:', err);
        res.status(500).send('Internal Server Error');
    }
});






app.post('/uploadvideo', upload.single('video'), (req, res) => {
  const id = genRandName();
  const userDir = path.join(__dirname, 'public', req.body.user || 'unknown');
  try {
    
    fs.mkdirSync(userDir, { recursive: true });

    if (!auth(req.body.user, req.body.password)) {
      res.status(200).json({ message: 'Incorrect and/or missing credentials'});
      console.log("invalid creds")
      fs.unlink('./public/'+req.file.filename, (err) => {console.log(err)});
      return
    }
      const fileName = id + getFileExtension(req.file.originalname);
      const filePath = path.join(userDir, fileName);
      
      fs.renameSync(req.file.path, filePath);
      
      console.log(`File uploaded successfully for user ${req.body.user}`);
      addVidJson("./backend/public/"+req.body.user+"/info.json", {name: req.body.title, id: id, compressed: false})
      compque.push({url: "http://localhost:3000/"+req.body.user+"/"+id+".mp4", compressionquality: "med"})
      console.log(compque)
      res.status(200).json({ message: 'Video uploaded successfully' });
    
  } catch (error) {
    console.error('Error uploading file:', error);
    res.status(500).json({ message: 'Failed to upload video', error: error.message });
  
    fs.unlink(__dirname +'/'+ req.file.path, (err) => {
      if (err) {
        console.error(`Error deleting file: ${err}`);
      } else {
        console.log('File deleted successfully');
      }
    });
  }
});

function validUsername(i) {
    return /^[a-z0-9_]+$/i.test(i);
}

function genRandName(length = 10) {
  const characters = 'abcdefghijklmnopqrstuvwxyz123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
      result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}

function getFileExtension(fstring) {
  return fstring.substring(fstring.lastIndexOf('.'));
}

function addVidJson(filePath, newElement) {
  // Read the JSON file
  console.log(filePath, newElement)
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error("Error reading the file:", err);
      return;
    }

    // Parse the JSON data
    let jsonData;
    try {
      jsonData = JSON.parse(data);
    } catch (err) {
      console.error("Error parsing JSON:", err);
      return;
    }

    // Check if the list exists in the JSON data
    if (!Array.isArray(jsonData.videos)) {
      console.error("List not found in the JSON data.");
      return;
    }

    // Add the new element to the list
    jsonData.videos.push(newElement);

    // Write the updated JSON back to the file
    fs.writeFile(filePath, JSON.stringify(jsonData, null, 2), 'utf8', (err) => {
      if (err) {
        console.error("Error writing to the file:", err);
      } else {
        console.log("New element added successfully.");
      }
    });
  });
}

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

