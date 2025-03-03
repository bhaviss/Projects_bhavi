const mongoose = require('mongoose');
const formSchema = new mongoose.Schema({
    Name: { type: String, required: true },
    Email: { type: String, required: true },
    ClassName: { type: String, required: true },
    location: { type: String, required: true }, // Check this field in your submission
}, {
    timestamps: true
});
const FormData = mongoose.model('FormData', formSchema);
module.exports = FormData;
