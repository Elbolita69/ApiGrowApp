const express = require('express');
const router = express.Router();
const pool = require('../config/database');

// GET /sensores-externos - List all
router.get('/', async (req, res, next) => {
    try {
        const result = await pool.query('SELECT * FROM sensores_externos WHERE estado = TRUE');
        res.json(result.rows);
    } catch (err) {
        next(err);
    }
});

// POST /sensores-externos - Create
router.post('/', async (req, res, next) => {
    try {
        const { tipo, valor_actual, ubicacion } = req.body;
        const result = await pool.query(
            'INSERT INTO sensores_externos (tipo, valor_actual, ubicacion, estado) VALUES ($1, $2, $3, TRUE) RETURNING *',
            [tipo, valor_actual, ubicacion]
        );
        res.status(201).json(result.rows[0]);
    } catch (err) {
        next(err);
    }
});

// GET /sensores-externos/:id - Get one
router.get('/:id', async (req, res, next) => {
    try {
        const result = await pool.query(
            'SELECT * FROM sensores_externos WHERE id = $1 AND estado = TRUE',
            [req.params.id]
        );
        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'Sensor no encontrado' });
        }
        res.json(result.rows[0]);
    } catch (err) {
        next(err);
    }
});

// PUT /sensores-externos/:id - Update
router.put('/:id', async (req, res, next) => {
    try {
        const { tipo, valor_actual, ubicacion } = req.body;
        const result = await pool.query(
            'UPDATE sensores_externos SET tipo = $1, valor_actual = $2, ubicacion = $3, actualizado = CURRENT_TIMESTAMP WHERE id = $4 AND estado = TRUE RETURNING *',
            [tipo, valor_actual, ubicacion, req.params.id]
        );
        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'Sensor no encontrado' });
        }
        res.json(result.rows[0]);
    } catch (err) {
        next(err);
    }
});

// DELETE /sensores-externos/:id - Soft delete
router.delete('/:id', async (req, res, next) => {
    try {
        const result = await pool.query(
            'UPDATE sensores_externos SET estado = FALSE, actualizado = CURRENT_TIMESTAMP WHERE id = $1 AND estado = TRUE RETURNING *',
            [req.params.id]
        );
        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'Sensor no encontrado' });
        }
        res.json({ message: 'Sensor eliminado' });
    } catch (err) {
        next(err);
    }
});

module.exports = router;
