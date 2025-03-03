const mongoose = require('mongoose');
const dbConfig = () => {
    mongoose.connect('mongodb+srv://Sindhu:Sindhu1234@cluster0.0pgzm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    .then(() => console.log('MongoDB connected!'))
    .catch(err => console.error('MongoDB connection error:', err));
};
module.exports=dbConfig;

