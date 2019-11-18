clear all
%close all

nome = 'Residencial_1pu';
curva1 = csvread(nome + ".csv");

% precisa declarar 25 pnts
curva1 = [curva1; curva1(end)];

pontos = 60;    % Número de pontos dentro de uma hora
division = 100;  % Altera a amplitude da variação

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
                c = c + 1;
            end         
        else
            c = (1+(p-1)*pontos);
            for k=a:(b-a)/(pontos-1):b
                r1(c) = k+rand(1)*10*(rand(1)-0.5)/division;
                if r1(c)<0, r1(c) = 0; end
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


csvwrite(nome + "_Minuto.csv", r1');