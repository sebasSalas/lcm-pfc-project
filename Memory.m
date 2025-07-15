function Memory
    clc;
    disp('Selecciona la opción a ejecutar:');
    disp('1. Mostrar tabla de escenarios');
    disp('2. Demostración de límite de memoria');
    disp('3. Ejecutar ambas');
    opcion = input('Opción (1/2/3): ');

    switch opcion
        case 1
            mostrar_tabla_escenarios();
        case 2
            demo_limite_memoria();
        case 3
            mostrar_tabla_escenarios();
            demo_limite_memoria();
        otherwise
            disp('Opción no válida.');
    end
end

function mostrar_tabla_escenarios()
    scenarios = { ...
        struct('name', 'Caso Base',   'n', 10, 'k', 5,  'max_val', 100), ...
        struct('name', 'Medio 1',     'n', 15, 'k', 5,  'max_val', 500), ...
        struct('name', 'Medio 2',     'n', 15, 'k', 7,  'max_val', 500), ...
        struct('name', 'Medio 3',     'n', 20, 'k', 5,  'max_val', 1000), ...
        struct('name', 'Medio-Alto',  'n', 20, 'k', 10, 'max_val', 1000), ...
        struct('name', 'Alto 1',      'n', 22, 'k', 11, 'max_val', 5000), ...
        struct('name', 'Alto 2',      'n', 25, 'k', 12, 'max_val', 5000), ...
        struct('name', 'Muy Alto',    'n', 28, 'k', 14, 'max_val', 10000), ...
        struct('name', 'Extremo',    'n', 32, 'k', 16, 'max_val', 10000) ...
    };

    fprintf('%-15s | %3s | %3s | %18s | %12s | %15s\n', ...
        'Escenario', 'n', 'k', 'Combinaciones', 'Tiempo (s)', 'Memoria (MB)');
    fprintf('%s\n', repmat('-', 1, 80));

    for i = 1:length(scenarios)
        s = scenarios{i};
        try
            S = randperm(s.max_val-2, s.n) + 1; % Equivalente a random.sample(range(2, max_val), n)
            % Medir memoria antes
            [~, sys] = memory;
            mem_before = sys.PhysicalMemory.Available;
            t_start = tic;
            C = nchoosek(S, s.k);
            elapsed = toc(t_start);
            [~, sys] = memory;
            mem_after = sys.PhysicalMemory.Available;
            mem_used = (mem_before - mem_after) / (1024^2); % en MB
            num_comb = size(C,1);
            fprintf('%-15s | %3d | %3d | %18d | %12.4f | %15.2f\n', ...
                s.name, s.n, s.k, num_comb, elapsed, mem_used);
        catch ME
            fprintf('%-15s | %3d | %3d | %18s | %12s | %15s\n', ...
                s.name, s.n, s.k, 'N/A', 'ERROR', 'N/A');
            disp(['Error en ' s.name ': ' ME.message]);
        end
    end
end

function demo_limite_memoria()
    % --- Parámetros de Entrada ---
    S = 1:32;
    k = 16;

    % --- Advertencia para el Usuario ---
    num_combinaciones = nchoosek(numel(S), k);
    memoria_estimada_gb = (num_combinaciones * k * 8) / (1024^3);

    fprintf('ADVERTENCIA: Este script intentará generar y almacenar en memoria:\n');
    fprintf('  - Número de combinaciones: %s\n', num2str(num_combinaciones, '%d'));
    fprintf('  - Tamaño de la matriz: %s x %d\n', num2str(num_combinaciones, '%d'), k);
    fprintf('  - Memoria estimada requerida: %.2f GB\n\n', memoria_estimada_gb);
    fprintf('Es muy probable que MATLAB se quede sin memoria y lance un error.\n');
    fprintf('Esto es deliberado y sirve para demostrar los límites de este enfoque.\n\n');

    pause(5);
    fprintf('Intentando la operación en 3... 2... 1...\n');
    disp(repmat('-', 1, 60));

    try
        tic;
        fprintf('Generando subconjuntos... (esto puede tardar o fallar)\n');
        subconjuntos = nchoosek(S, k);
        tiempo_transcurrido = toc;
        fprintf('¡Éxito! La operación se completó (esto requiere mucha RAM).\n');
        fprintf('Tiempo transcurrido: %.2f segundos.\n', tiempo_transcurrido);
        info_variable = whos('subconjuntos');
        memoria_usada_gb = info_variable.bytes / (1024^3);
        fprintf('--- Detalles de la Variable en Memoria ---\n');
        fprintf('Nombre de la variable: %s\n', info_variable.name);
        fprintf('Dimensiones: %d x %d\n', info_variable.size(1), info_variable.size(2));
        fprintf('Memoria utilizada: %.2f GB\n', memoria_usada_gb);
    catch ME
        disp(repmat('-', 1, 60));
        fprintf('\n¡ERROR CAPTURADO!\n');
        fprintf('Tal como se esperaba, la operación ha fallado.\n');
        if strcmp(ME.identifier, 'MATLAB:nomem')
            fprintf('Causa del error: MATLAB se ha quedado sin memoria RAM disponible.\n');
            fprintf('Esto demuestra que almacenar %s combinaciones en memoria no es viable.\n', num2str(num_combinaciones, '%d'));
        else
            fprintf('Se ha producido un error inesperado:\n');
            disp(ME.message);
        end
    end
end 