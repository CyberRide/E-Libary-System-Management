<?php

/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', "mspssone_item" );

/** Database username */
define( 'DB_USER', "mspssone_item" );

/** Database password */
define( 'DB_PASSWORD', "item@#12" );

/** Database hostname */
define( 'DB_HOST', "server20.mysql-host.eu" );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         '%W,1f^  &;r}iAw%a+d:n6!lKbH}8w]lN)aL,7W9[D^{x6C?Lj7e!%{j1<b4[GCf' );
define( 'SECURE_AUTH_KEY',  '?+JRx()x];NaTq|}KK#ww?r0HN$>rXCnP1?hW?>*H}v](_Y:1aG-|]!kh>}7gW,/' );
define( 'LOGGED_IN_KEY',    '[F9gPA#6OB:34Le<]{&~wM9{|6Z}feEx;j1YY|4lzX<e&>xJwH//PS3pvz6Q_Er(' );
define( 'NONCE_KEY',        'st 8l}m$w|@x3lG;;#bXH.LzyjzEY9y,*cxw05ooVI;~Q[3>F>:!TEH6) ?VA>IF' );
define( 'AUTH_SALT',        'KPtw]7x;BE{h$LY/GFXR;55`@(Tjl&v!Vu16-?q_{4-yUs/7pd ?:e XTzD&?z}S' );
define( 'SECURE_AUTH_SALT', '])O}V9#|59ZJ!R*K=V4vLBBi;!gnoz@.^/AViW<-1Suq.A@o[Hha=#z@q;t~=|q-' );
define( 'LOGGED_IN_SALT',   'n Nd(jGq%H*2LbCqN%uJA4NU-rQ~|`sL)<LinV:V{VDr7i{!91Ge{i~qkF63XzI[' );
define( 'NONCE_SALT',       'M!]^^/JD4GmT]88flmv5hk$E%+xRir8v aToW@IR?n2y#,0wq]el%6(;PDPv-Mw6' );

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );

/* Add any custom values between this line and the "stop editing" line. */



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', dirname(__FILE__) . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
