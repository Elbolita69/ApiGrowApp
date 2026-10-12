const express = require('express');
const router = express.Router();
const pool = require('../config/database');

router.get('/', async (req, res, next) => {
    try {
        const [rows] = await pool.query('SELECT * FROM lecturas_externas WHERE estado = TRUE ORDER BY timestamp DESC');
        res.json(rows);
    } catch (err) {
        next(err);
    }
});

router.post('/', async (req, res, next) => {
    try {
        const { sensor_id, valor, timestamp } = req.body;
        const [result] = await pool.query(
            'INSERT INTO lecturas_externas (sensor_id, valor, timestamp, estado) VALUES (?, ?, ?, TRUE)',
            [sensor_id, valor, timestamp || new Date()]
        );
        const [rows] = await pool.query('SELECT * FROM lecturas_externas WHERE id = ?', [result.insertId]);
        res.status(201).json(rows[0]);
    } catch (err) {
        next(err);
    }
});

module.exports = router;
