clear all
close all

%nome_arquivo = 'Loadshape';
%nome_arquivo = 'Temperatura';
nome_arquivo = 'Irradiacao';

curva1 = csvread(nome_arquivo + ".csv");

%curva1 = [0.33 0.29 0.25 0.23 0.22 0.31 0.42 0.44 0.40 0.43 0.51 0.51 0.53 0.42 0.40 0.45 0.45 0.62 0.78 0.98 1.00 0.83 0.78 0.47 0.47]; % Res1
%curva1 = [0.69000000 0.50999999 0.44999999 0.41999999 0.55000001 0.85000002 1.01999998 0.80000001 0.89999998 0.91000003 1.02999997 1.03999996 1.11000001 0.98000002 0.94000000 0.94000000 1.02999997 1.26999998 1.51999998 1.59000003 1.75999999 1.50999999 1.29999995  0.89999998 0.8]
% precisa declarar 25 pnts

pontos = 60;    % Número de pontos dentro de uma hora
division = 200;  % Altera a amplitude da variação

x = [0:(length(curva1)-1)/((pontos)*(length(curva1)-1)-1):(length(curva1)-1)];

% For que vai do primeiro ponto até o 23 de curva
for p=1:(length(curva1)-1)
%  p=2
    a = curva1(p);
    b = curva1(p+1);
    if (a == b) && (a == 0)
        r1((1+(p-1)*pontos):((p-1)*pontos+pontos)) = a*zeros(pontos,1)'; 
    else
        if a==b
    %        r((1+(p-1)*pontos):((p-1)*pontos+pontos)) = a*ones(pontos,1)'; 
            c = (1+(p-1)*pontos);
            for k=1:pontos
                r1(c) = a + rand(1)*10*(rand(1)-0.5)/division;
                if r1(c)<0, r1(c) = 0; end
                if nome_arquivo == "Loadshape"
                    if r1(c)>1, r1(c) = 1; end
                end
                c = c + 1;
            end         
        else
            c = (1+(p-1)*pontos);
            for k=a:(b-a)/(pontos-1):b
                r1(c) = k+rand(1)*10*(rand(1)-0.5)/division;
                if r1(c)<0, r1(c) = 0; end
                if nome_arquivo == "Loadshape"
                    if r1(c)>1, r1(c) = 1; end
                end
                c = c + 1;
            end
        end
    end
end

% for p=1:(length(curva1)-1)
%  p=2
%     a = curva1(p);
%     b = curva1(p+1);
%     if a==b&&a==0
%         r1((1+(p-1)*pontos):((p-1)*pontos+pontos)) = a*zeros(pontos,1)'; 
%     else
%         if a==b
%            r((1+(p-1)*pontos):((p-1)*pontos+pontos)) = a*ones(pontos,1)'; 
%             c = (1+(p-1)*pontos);
%             for k=1:pontos
%                 r1(c) = a + rand(1)*10*(rand(1)-0.5)/division;
%                 if r1(c)<0, r1(c) = 0; end
%                 c = c + 1;
%             end         
%         else
%             c = (1+(p-1)*pontos);
%             for k=a:(b-a)/(pontos-1):b
%                 r1(c) = k+rand(1)*10*(rand(1)-0.5)/division;
%                 if r1(c)<0, r1(c) = 0; end
%                 c = c + 1;
%             end
%         end
%     end
% end

% %
plot(x,r1)
hold on
plot(0:24,curva1)

% Gera arquivo DSS com o loadshape
% Necessário alterar o nome loadshape_nova.dss a cada nova curva
% arquivo  = fopen('LoadshapeVE.dss','wt');
% 
% fprintf(arquivo,'New Loadshape.VE npts=1440 interval=1 mult=(',r1);
% fprintf(arquivo,'%1.4f ',r1);
% fprintf(arquivo,')\n',r1);
% 
% arquivo = fclose(arquivo);

csvwrite(nome_arquivo + "_1440.csv", r1');