const mysql = require('mysql2/promise');
const { construirConfig } = require('./opciones');

const pool = mysql.createPool(construirConfig(process.env));

module.exports = pool;
