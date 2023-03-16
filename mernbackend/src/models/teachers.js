const mongoose=require("mongoose");

const staffdetails=new mongoose.Schema({
   
    temailid:{
        type: String,
        required:true
    },
    tpassword:{
        type: String,
        required:true
    },
   
})

const Teacher=new mongoose.model("Teacher",staffdetails);
module.exports=Teacher;