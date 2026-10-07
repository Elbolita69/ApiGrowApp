const express = require('express');
const router = express.Router();
const pool = require('../config/database');

// GET /lecturas-externas - List all
router.get('/', async (req, res, next) => {
    try {
        const result = await pool.query('SELECT * FROM lecturas_externas WHERE estado = TRUE ORDER BY timestamp DESC');
        res.json(result.rows);
    } catch (err) {
        next(err);
    }
});

// POST /lecturas-externas - Create
router.post('/', async (req, res, next) => {
    try {
        const { sensor_id, valor, timestamp } = req.body;
        const result = await pool.query(
            'INSERT INTO lecturas_externas (sensor_id, valor, timestamp, estado) VALUES ($1, $2, $3, TRUE) RETURNING *',
            [sensor_id, valor, timestamp || new Date()]
        );
        res.status(201).json(result.rows[0]);
    } catch (err) {
        next(err);
    }
});

module.exports = router;
