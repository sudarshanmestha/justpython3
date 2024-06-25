/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.{html,js}',
        '../justpythonin/templates/**/*.{html,js}',
        // Include JavaScript files that might contain Tailwind CSS classes
        // '../static/**/*.js',
        // '../static/**/*.css',
    ],
    theme: {
        extend: {
            textDecorationThickness: {
                3: '3px',
              }
        },
        fontSize: {
            sm: '0.8rem',
            base: '1rem',
            xl: '1.25rem',
            '2xl': '1.563rem',
            '3xl': '1.953rem',
            '4xl': '2.441rem',
            '5xl': '3.052rem',
          }
        }
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
      ],
};
