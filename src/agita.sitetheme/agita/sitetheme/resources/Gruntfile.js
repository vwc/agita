/* jshint node: true */
'use strict';

module.exports = function (grunt) {

    // load all grunt tasks
    require('load-grunt-tasks')(grunt);

    // Project configuration.
    grunt.initConfig({

        // Metadata.
        pkg: grunt.file.readJSON('package.json'),
        banner: '/*!\n' +
                  '* <%= pkg.name %> v<%= pkg.version %> by Ade25\n' +
                  '* Copyright <%= pkg.author %>\n' +
                  '* Licensed under <%= pkg.licenses %>.\n' +
                  '*\n' +
                  '* Designed and built by ade25\n' +
                  '*/\n',
        jqueryCheck: 'if (typeof jQuery === "undefined") { throw new Error(\"We require jQuery\") }\n\n',

        // Task configuration.
        clean: {
            dist: ['dist']
        },

        jshint: {
            options: {
                jshintrc: 'js/.jshintrc'
            },
            gruntfile: {
                src: 'Gruntfile.js'
            },
            src: {
                src: ['js/*.js']
            },
            test: {
                src: ['js/tests/unit/*.js']
            }
        },

        concat: {
            options: {
                banner: '<%= banner %>',
                stripBanners: false
            },
            dist: {
                src: [
                    'bower_components/jquery/dist/jquery.js',
                    'bower_components/modernizr/modernizr.js',
                    'bower_components/bootstrap/dist/js/bootstrap.js',
                    'bower_components/holderjs/holder.js',
                    'js/main.js'
                ],
                dest: 'dist/js/<%= pkg.name %>.js'
            },
            theme: {
                src: [
                    'bower_components/bootstrap/dist/js/bootstrap.js',
                    'bower_components/slabText/js/jquery.slabtext.js',
                    'js/main.js'
                ],
                dest: 'dist/js/main.js'
            }
        },

        uglify: {
            options: {
                banner: '<%= banner %>'
            },
            dist: {
                src: ['<%= concat.dist.dest %>'],
                dest: 'dist/js/<%= pkg.name %>.min.js'
            }
        },

        less: {
            compileTheme: {
                options: {
                    strictMath: false,
                    sourceMap: true,
                    outputSourceFiles: true,
                    sourceMapURL: '<%= pkg.name %>.css.map',
                    sourceMapFilename: 'dist/css/<%= pkg.name %>.css.map'
                },
                files: {
                    'dist/css/<%= pkg.name %>.css': 'less/styles.less'
                }
            },
            minify: {
                options: {
                    cleancss: true,
                    report: 'min'
                },
                files: {
                    'dist/css/<%= pkg.name %>.min.css': 'dist/css/<%= pkg.name %>.css'
                }
            }
        },

        csscomb: {
            sort: {
                options: {
                    config: 'less/.csscomb.json'
                },
                files: {
                    'dist/css/<%= pkg.name %>.css': ['dist/css/<%= pkg.name %>.css']
                }
            }
        },

        copy: {
            fonts: {
                expand: true,
                flatten: true,
                cwd: 'bower_components/',
                src: ['font-awesome/fonts/*'],
                dest: 'dist/assets/fonts/'
            },
            ico: {
                expand: true,
                flatten: true,
                cwd: 'bower_components/',
                src: ['bootstrap/assets/ico/*'],
                dest: 'dist/assets/ico/'
            },
            images: {
                expand: true,
                flatten: true,
                src: ['assets/img/*'],
                dest: 'dist/assets/img/'
            },
            favicon: {
                expand: true,
                flatten: true,
                src: ['assets/ico/*'],
                dest: 'dist/assets/ico/'
            }
        },

        imagemin: {
            dynamic: {
                files: [{
                    expand: true,
                    cwd: 'assets/img/',
                    src: ['**/*.{png,jpg,gif}'],
                    dest: 'dist/assets/img/'
                }]
            }
        },

        rev: {
            options:  {
                algorithm: 'sha256',
                length: 8
            },
            files: {
                src: ['dist/**/*.{js,css,png,jpg}']
            }
        },
        qunit: {
            options: {
                inject: 'js/tests/unit/phantom.js'
            },
            files: ['js/tests/*.html']
        },

        connect: {
            server: {
                options: {
                    port: 3000,
                    base: '.'
                }
            }
        },
        jekyll: {
            theme: {}
        },

        sed: {
            cleanSourceAssets: {
                path: 'dist/',
                pattern: '../../assets/',
                replacement: '../assets/',
                recursive: true
            },
            cleanSourceCSS: {
                path: 'dist/',
                pattern: '../dist/css/agita.css',
                replacement: 'css/agita.css',
                recursive: true
            },
            cleanSourceJS: {
                path: 'dist/',
                pattern: '../dist/js/agita.js',
                replacement: 'js/agita.min.js',
                recursive: true
            },
            cleanLogo: {
                path: 'dist/',
                pattern: '../assets/img/logo.png',
                replacement: 'assets/img/logo.png',
                recursive: true
            },
            cleanBrandlogo: {
                path: 'dist/',
                pattern: '../assets/img/kinderschutzbund.png',
                replacement: 'assets/img/kinderschutzbund.png',
                recursive: true
            },
            cleanContactTag: {
                path: 'dist/',
                pattern: '../assets/img/contact-tag.png',
                replacement: 'assets/img/contact-tag.png',
                recursive: true
            },
            cleanFooterLogo01: {
                path: 'dist/',
                pattern: '../assets/img/logo-stadt-augsburg.png',
                replacement: 'assets/img/logo-stadt-augsburg.png',
                recursive: true
            },
            cleanFooterFaces: {
                path: 'dist/',
                pattern: '../assets/img/faces.png',
                replacement: 'assets/img/faces.png',
                recursive: true
            }
        },

        validation: {
            options: {
                charset: 'utf-8',
                doctype: 'HTML5',
                failHard: true,
                reset: true,
                relaxerror: [
                    'Bad value X-UA-Compatible for attribute http-equiv on element meta.',
                    'Element img is missing required attribute src.'
                ]
            },
            files: {
                src: ['_site/**/*.html']
            }
        },

        watch: {
            src: {
                files: '<%= jshint.src.src %>',
                tasks: ['jshint:src', 'qunit']
            },
            test: {
                files: '<%= jshint.test.src %>',
                tasks: ['jshint:test', 'qunit']
            },
            less: {
                files: 'less/*.less',
                tasks: ['less'],
                options: {
                    spawn: false
                }
            }
        },

        concurrent: {
            cj: ['less', 'copy', 'concat', 'uglify'],
            ha: ['jekyll:theme', 'copy-templates', 'sed']
        }

    });


    // -------------------------------------------------
    // These are the available tasks provided
    // Run them in the Terminal like e.g. grunt dist-css
    // -------------------------------------------------

    // Prepare distrubution
    grunt.registerTask('dist-init', '', function () {
        grunt.file.mkdir('dist/assets/');
    });

    // Copy jekyll generated templates and rename for diazo
    grunt.registerTask('copy-templates', '', function () {
        grunt.file.copy('_site/index.html', 'dist/theme.html');
        grunt.file.copy('_site/signin/index.html', 'dist/signin.html');
        grunt.file.copy('_site/panelpage/index.html', 'dist/panelpage.html');
    });

    // Docs HTML validation task
    grunt.registerTask('validate-html', ['jekyll', 'validation']);

    // Javascript Unittests
    grunt.registerTask('unit-test', ['qunit']);

    // Test task.
    var testSubtasks = ['dist-css', 'jshint', 'validate-html'];

    grunt.registerTask('test', testSubtasks);

    // JS distribution task.
    grunt.registerTask('dist-js', ['concat', 'uglify']);

    // CSS distribution task.
    grunt.registerTask('less-compile', ['less:compileTheme']);
    grunt.registerTask('dist-css', ['less-compile', 'csscomb', 'less:minify']);

    // Assets distribution task.
    grunt.registerTask('dist-assets', ['newer:copy', 'newer:imagemin']);

    // Cache buster distribution task.
    grunt.registerTask('dist-cb', ['rev']);

    // Template distribution task.
    grunt.registerTask('dist-html', ['jekyll:theme', 'copy-templates', 'sed']);

    // Concurrent distribution task
    grunt.registerTask('dist-cc', ['test', 'concurrent:cj', 'concurrent:ha']);

    // Development task.
    grunt.registerTask('dev', ['less-compile', 'dist-js', 'dist-html']);

    // Full distribution task.
    grunt.registerTask('dist', ['clean', 'dist-css', 'dist-js', 'dist-html', 'dist-assets']);

    // Shim theme compilation alias
    grunt.registerTask('compile-theme', ['dist']);

    // Default task.
    grunt.registerTask('default', ['dev']);

};