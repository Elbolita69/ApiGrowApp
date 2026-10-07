const express = require('express');
const router = express.Router();
const pool = require('../config/database');

router.get('/', async (req, res, next) => {
    try {
        const result = await pool.query('SELECT * FROM alertas_externas WHERE estado = TRUE');
        res.json(result.rows);
    } catch (err) {
        next(err);
    }
});

router.post('/', async (req, res, next) => {
    try {
        const { mensaje, prioridad } = req.body;
        const result = await pool.query(
            'INSERT INTO alertas_externas (mensaje, prioridad, estado) VALUES ($1, $2, TRUE) RETURNING *',
            [mensaje, prioridad || 'media']
        );
        res.status(201).json(result.rows[0]);
    } catch (err) {
        next(err);
    }
});

router.put('/:id', async (req, res, next) => {
    try {
        const { mensaje, prioridad } = req.body;
        const result = await pool.query(
            'UPDATE alertas_externas SET mensaje = $1, prioridad = $2, actualizado = CURRENT_TIMESTAMP WHERE id = $3 AND estado = TRUE RETURNING *',
            [mensaje, prioridad, req.params.id]
        );
        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'Alerta no encontrada' });
        }
        res.json(result.rows[0]);
    } catch (err) {
        next(err);
    }
});

router.delete('/:id', async (req, res, next) => {
    try {
        const result = await pool.query(
            'UPDATE alertas_externas SET estado = FALSE, actualizado = CURRENT_TIMESTAMP WHERE id = $1 AND estado = TRUE RETURNING *',
            [req.params.id]
        );
        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'Alerta no encontrada' });
        }
        res.json({ message: 'Alerta eliminada' });
    } catch (err) {
        next(err);
    }
});

module.exports = router;
