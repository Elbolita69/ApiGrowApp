const MODOS_CON_TLS = ['required', 'verify_ca', 'verify_identity'];

function construirConfig(env) {
    const crudo = (env.MYSQL_URL || '').trim();
    if (!crudo) {
        throw new Error('Falta MYSQL_URL en express-api/.env (o en las variables de Render).');
    }

    const url = new URL(crudo);
    const modo = (url.searchParams.get('ssl-mode') || url.searchParams.get('sslmode') || '').toLowerCase();
    const forzado = (env.MYSQL_SSL || '').trim().toLowerCase() === 'true';

    const config = {
        host: url.hostname,
        port: Number(url.port) || 3306,
        user: decodeURIComponent(url.username),
        password: decodeURIComponent(url.password),
        database: decodeURIComponent(url.pathname.replace(/^\//, '')),
        waitForConnections: true,
        connectionLimit: Number(env.MYSQL_POOL_MAX) || 5,
        queueLimit: 0,
        timezone: 'local'
    };

    if (forzado || MODOS_CON_TLS.includes(modo)) {
        config.ssl = { rejectUnauthorized: false };
    }
    return config;
}

module.exports = { construirConfig };
