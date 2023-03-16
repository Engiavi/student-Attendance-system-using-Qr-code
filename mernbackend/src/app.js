
const express = require("express");
// const download = require('download');
const mongoose = require("mongoose");
const path = require("path");
const app = express();
const hbs = require("hbs");
const Register = require("./models/registers");
const Teacher = require("./models/teachers");
const DB = "mongodb://127.0.0.1:27017/student";
// const fs = require('fs');
const qrcode = require('qrcode');

const { PythonShell } = require('python-shell');

mongoose.connect(DB, {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => { console.log(`connection successful`); }).catch((e) => {
  console.log(`no connection`);
})
const port = process.env.PORT || 3000;

const static_path = path.join(__dirname, "../New");
const excel_path = path.join(__dirname, "../excel");
const view_path = path.join(__dirname, "../templates/views");
const partials_path = path.join(__dirname, "../templates/partials");
app.set("view engine", "hbs");
hbs.registerPartials(partials_path);

app.use(express.static(static_path));

app.set("views", view_path);

app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.get("/", (req, res) => {
  res.render("index")
});
app.get("/index", (req, res) => {
  res.render("index")
});
app.get("/login", (req, res) => {
  res.render("login");
});
app.get("/register", (req, res) => {
  res.render("register");
});
app.get("/staff", (req, res) => {
  res.render("staff");
});
app.get("/staffdetails", (req, res) => {
  res.render("staffdetails");
});
app.get("/run_python", (req, res) => {
  res.render("run_python");
});
app.get("/run_excel", (req, res) => {
  res.render("run_excel");
});
app.get("/afterlogin", (req, res) => {
  res.render("afterlogin");
});

app.post("/run_python", async (req, res) => {
  PythonShell.run('New/scanner.py', {}, (error, results) => {
    if (error) {
      res.send({ success: false, error: error });
    } else {
      res.send({ success: true, results: results });
    }
  });
});
app.post("/register", async (req, res) => {
  try {
    const password = req.body.password;
    const cpassword = req.body.confirmpassword;
    if (password === cpassword) {
      const registerEmployee = new Register({
        firstname: req.body.firstname,
        lastname: req.body.lastname,
        gender: req.body.gender,
        mobileno: req.body.mobileno,
        rollno: req.body.rollno,
        emailid: req.body.emailid,
        password: req.body.password,
        confirmpassword: req.body.confirmpassword
      })

      const registered = await registerEmployee.save();
      res.status(201).render("login");

    } else {
      res.send("PASSWORD NOT MATCH");
    }

  } catch (error) {
    res.status(440).send(error)

  }
});
let firstN = "";
app.post("/login", async (req, res) => {
  try {
    const emailid = req.body.emailid;
    const password = req.body.password;
    const useremail = await Register.findOne({ emailid: emailid });
    if (!useremail) {
      res.status(400).send("<script>alert('Invalid Email Id');</script>");
      return;
    }
    if (useremail.password === password) {
      const qrData = {
        firstname: useremail.firstname,
        lastname: useremail.lastname,
        emailid: useremail.emailid,
      };
      const first = qrData.firstname;
      firstN = first;
      const qrCodeImage = await qrcode.toDataURL(JSON.stringify(qrData));
      res.status(201).render("afterlogin", { qrCodeImage, first });
    } else {
      res.send("<script>alert('Invalid Password');</script>");
    }
  } catch (error) {
    res.status(400).send("404 error");
  }
});
app.post("/run_excel", async (req, res) => {
  let a = firstN;

  const options = {
    args: [a]
  };
  console.log(options)
  PythonShell.run('New/excel.py', options, (error, results) => {
    console.log(error, results)
    if (error) {
      res.send({ success: false, error: error });
    } else {
      res.send({ success: true, results: results });
    }
  });
});
console.log(firstN)


app.post("/staff", async (req, res) => {
  try {
    const temailid = req.body.temailid;
    const tpassword = req.body.tpassword;

    const tearemail = await Teacher.findOne({ temailid: temailid });
    if (tearemail.tpassword === tpassword) {
      res.status(201).render('staffdetails');
    }
    else {
      res.send('invalid login details');
    }
  } catch (error) {
    res.status(400).send('404 error');
  }
});

app.listen(port, () => {
  console.log(`server is running at port ${port}`);
});