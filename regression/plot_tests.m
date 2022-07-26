%% White

% add a folder name to add a test
test_list = ["test_White2004_4000-1", ...
             "test_White2004_4000-2", ...
             "test_White2004_4000-3", ...
             "test_White2004_4000-4", ...
             "test_White2004_4000-5", ...
             "test_White2004_4004-1", ...
             "test_White2004_4004-2", ...
             "test_White2004_4004-3", ...
             "test_White2004_4004-4", ...
             "test_White2004_4004-5", ...
             "test_White2004_4004-6", ...
             "test_White2004_4005-1", ...
             "test_White2004_4005-2", ...
             "test_White2004_4005-3", ...
             "test_White2004_4005-4", ...
             "test_White2004_4005-5", ...
             "test_White2004_4064-1", ...
             "test_White2004_4064-2", ...
             "test_White2004_4064-3", ...
             "test_White2004_4064-4", ...
             "test_White2004_4064-5", ...
             "test_White2004_4065-1", ...
             "test_White2004_4065-2", ...
             "test_White2004_4065-3", ...
             "test_White2004_4065-4", ...
             "test_White2004_4065-5", ...
             "test_White2004_4135-1", ...
             "test_White2004_4135-2", ...
             "test_White2004_4135-3", ...
             "test_White2004_4136-1", ...
             "test_White2004_4136-2", ...
             "test_White2004_4136-3", ...
             "test_White2004_4136-4", ...
             "test_White2004_4140-1", ...
             "test_White2004_4140-2", ...
             "test_White2004_4162-1", ...
             "test_White2004_4162-2", ...
             "test_White2004_4162-3", ...
             "test_White2004_4162-4", ...
             "test_White2004_4163-1", ...
             "test_White2004_4163-2", ...
             "test_White2004_4163-3", ...
             "test_White2004_4163-4", ...
             ];

test_num  = length(test_list);

root = strcat(pwd,"\");

destination_path = strcat(root,test_list(1),'\');
cd(destination_path)
output_file = importdata('output.txt');
length_output = numel(output_file.colheaders);
output_file = importdata('output_gold.txt');
length_output_gold = numel(output_file.colheaders);
cd ..

%% output.txt
% positions of interest
for jj = 1:length_output
    destination_path = strcat(root,test_list(1),'\');
    cd(destination_path)
    output_file = importdata('output.txt');
    if(output_file.colheaders(1, jj) == "Intragranular gas swelling (/)")
        ig_swelling_col = jj;
    end
    if(output_file.colheaders(1, jj) == "Intergranular gas swelling (/)")
        gb_swelling_col = jj;
    end
    cd ..
end

% import grain-boundary swelling from output.txt
for jj = 1:test_num
    destination_path = strcat(root,test_list(jj),'\');
    cd(destination_path)
    output_file = importdata('output.txt');
    % N_output(jj) = output_file.data(end,21);
    % R_output(jj) = output_file.data(end,24);
    gb_swelling_test(jj) = output_file.data(end,gb_swelling_col) * 100;    
    cd ..
end

%% output_gold.txt
% positions of interest
for jj = 1:length_output_gold
    destination_path = strcat(root,test_list(1),'\');
    cd(destination_path)
    output_file = importdata('output_gold.txt');
    if(output_file.colheaders(1, jj) == "Intragranular gas swelling (/)")
        ig_swelling_col = jj;
    end
    if(output_file.colheaders(1, jj) == "Intergranular gas swelling (/)")
        gb_swelling_col = jj;
    end
    cd ..
end

% import grain-boundary swelling from output_gold.txt
for jj = 1:test_num
    destination_path = strcat(root,test_list(jj),'\');
    cd(destination_path)
    output_file = importdata('output_gold.txt');
    % N_output_gold(jj) = output_file.data(end,21);
    % R_output_gold(jj) = output_file.data(end,24);
    gb_swelling_gold(jj) = output_file.data(end,gb_swelling_col) * 100;    
    cd ..
end

% experimental data
gb_swelling_white = [0.97, 0.68, 0.53, 0.46, 0.17, ... % 4000
    0.62, 0.7, 0.44, 0.56, 0.27, 0.16, ...             % 4004
    0.94, 0.57, 0.42, 0.54, 0.27, ...                  % 4005 
    1.07, 0.86, 0.63, 0.74, 0.59, ...                  % 4064
    1.25, 1.35, 0.97, 0.79, 0.21  ...                  % 4065
    0.42, 0.16, 0.09, ...                              % 4135
    0.6, 0.62, 0.26, 0.11, ...                         % 4136
    0.26, 0.18, ...                                    % 4140
    0.7, 0.46, 0.43, 0.43, ...                         % 4162
    0.6, 0.59, 0.35, 0.4, ...                          % 4163
    ];

% 1.0 data
gb_swelling_1_0 = [1.19, 1.16, 1.13, 1.12, 1.29, ...   % 4000
    0.91, 0.89, 0.85, 0.79, 0.77, 0.81, ...            % 4004
    0.89, 0.87, 0.82, 0.76, 0.79, ...                  % 4005
    1.89, 1.83, 1.68, 1.46, 1.33, ...                  % 4064
    1.52, 1.48, 1.41, 1.35, 1.31, ...                  % 4065
    0.79, 0.79, 0.77, ...                              % 4135
    0.83, 0.83, 0.81, 0.79, ...                        % 4136
    0.87, 0.86, ...                                    % 4140
    1.72, 1.69, 1.62, 1.49, ...                        % 4162
    0.85, 0.84, 0.83, 0.82, ...                        % 4163
    ];

figure
p1 = loglog(gb_swelling_white, gb_swelling_1_0,'r.','MarkerSize',16);
hold on
p2 = loglog(gb_swelling_white, gb_swelling_gold,'g.','MarkerSize',16);
hold on
p3 = loglog(gb_swelling_white, gb_swelling_test,'k+','MarkerSize',16);
hold on
plot([10^-3 10^2],[10^-3 10^2],'k-')
hold on
plot([10^-3 10^2],[2*10^-3 2*10^2],'k--')
hold on
plot([10^-3 10^2],[0.5*10^-3 0.5*10^2],'k--')
hold on
title('Inter-granular bubble swelling %')
ylabel('Simulated (%)')
xlabel('Experimental (%)')
xlim([10^-3 10^2])
ylim([10^-3 10^2])
legend([p1 p2 p3],{'SCIANTIX 1.0','SCIANTIX 2.0 gold', 'SCIANTIX 2.0 test'},'location','NorthWest')

% saveas(gcf,'White et al 2006.png');

%% Baker
test_list = ["test_Baker1977__1273K", ...
             "test_Baker1977__1373K", ...
             "test_Baker1977__1473K", ...
             "test_Baker1977__1573K", ...
             "test_Baker1977__1673K", ...
             "test_Baker1977__1773K", ...
             "test_Baker1977__1873K", ...
             "test_Baker1977__1973K", ...
             "test_Baker1977__2073K"];

test_num  = length(test_list);

root = strcat(pwd,"\");

%% output.txt
% positions of interest
for jj = 1:length_output
    destination_path = strcat(root,test_list(1),'\');
    cd(destination_path)
    output_file = importdata('output.txt');
    if(output_file.colheaders(1, jj) == "Intragranular gas swelling (/)")
        ig_swelling_col = jj;
    end
    if(output_file.colheaders(1, jj) == "Intergranular gas swelling (/)")
        gb_swelling_col = jj;
    end
    cd ..
end

for jj = 1:test_num
    destination_path = strcat(root,test_list(jj),'\');
    cd(destination_path)
    output_file = importdata('output.txt');
    % N_output(jj) = output_file.data(end,18);
    % R_output(jj) = output_file.data(end,19);
    ig_swelling_test(jj) = output_file.data(end,ig_swelling_col) * 100;    
    cd ..
end

%% output_gold.txt
for jj = 1:length_output_gold
    destination_path = strcat(root,test_list(1),'\');
    cd(destination_path)
    output_file = importdata('output_gold.txt');
    if(output_file.colheaders(1, jj) == "Intragranular gas swelling (/)")
        ig_swelling_col = jj;
    end
    if(output_file.colheaders(1, jj) == "Intergranular gas swelling (/)")
        gb_swelling_col = jj;
    end
    cd ..
end

for jj = 1:test_num
    destination_path = strcat(root,test_list(jj),'\');
    cd(destination_path)
    output_file = importdata('output_gold.txt');
    % N_output(jj) = output_file.data(end,18);
    % R_output(jj) = output_file.data(end,19);
    ig_swelling_gold(jj) = output_file.data(end,ig_swelling_col) * 100;    
    cd ..
end

ig_swelling_1_0 = [0.033, 0.048, 0.062, 0.073, 0.079, 0.082, 0.083, 0.084, 0.086];
ig_swelling_baker = [0.06, 0.07, 0.08, 0.09, 0.12, 0.15, 0.18, 0.24, 0.31];

figure
p1 = loglog(ig_swelling_baker, ig_swelling_1_0,'r.','MarkerSize',16);
hold on
p2 = loglog(ig_swelling_baker, ig_swelling_gold,'g.','MarkerSize',16);
hold on
p3 = loglog(ig_swelling_baker, ig_swelling_test,'k+','MarkerSize',16);
hold on
plot([10^-3 10^2],[10^-3 10^2],'k-')
hold on
plot([10^-3 10^2],[2*10^-3 2*10^2],'k--')
hold on
plot([10^-3 10^2],[0.5*10^-3 0.5*10^2],'k--')
hold on
title('Intra-granular bubble swelling %')
ylabel('Simulated (%)')
xlabel('Experimental (%)')
xlim([10^-3 10^2])
ylim([10^-3 10^2])
legend([p1 p2 p3],{'SCIANTIX 1.0','SCIANTIX 2.0 gold', 'SCIANTIX 2.0 test'},'location','NorthWest')

% saveas(gcf,'Baker 1977.png');