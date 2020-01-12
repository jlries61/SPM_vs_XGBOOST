% Script to convert DEXTER dataset with initial format to usual csv.
clear;

% Uncomment needed code block (for train or test)
% ---------------------------------------------------------------
% filename_from_data = [pwd filesep 'dexter_train.data'];
% filename_from_labels = [pwd filesep 'dexter_train.labels'];
% filename_to = [pwd filesep 'dexter_train.csv'];
% ---------------------------------------------------------------
filename_from_data = [pwd filesep 'dexter_valid.data'];
filename_from_labels = [pwd filesep 'dexter_valid.labels'];
filename_to = [pwd filesep 'dexter_test.csv'];
% ---------------------------------------------------------------

N_features = 20000;
N_samples = 300;

header = cell(1,N_features);
for i = 1:N_features
    header{i} = ['x' num2str(i)];
end;
header = [strjoin(header,',') ',' 'class' '\n'];

fid_data = fopen(filename_from_data,'r');
fid_labels = fopen(filename_from_labels,'r');
fid_csv = fopen(filename_to,'w');

fprintf(fid_csv,header,[]);

for i = 1:N_samples
    tline_data = fgetl(fid_data);
    tline_labels = fgetl(fid_labels);
    
    if strcmp(tline_labels,'-1')
        tline_labels = '0';
    end;
    
    line_data_old = strsplit(tline_data,' ');
    line_data_new = cell(1,N_features);
    line_data_new(:) = {''};
    for j = 1:length(line_data_old)
        if any(line_data_old{j})
            cell_value = strsplit(line_data_old{j},':');
            line_data_new{str2double(cell_value{1})} = cell_value{2};
        end;
    end;
    line_data_new = [strjoin(line_data_new,',') ',' tline_labels '\n'];
    
    fprintf(fid_csv,line_data_new,[]);
    
    disp([num2str(i/N_samples*100,'%.2f') '% done.']);
end;
disp('Finished.');

fclose(fid_data);
fclose(fid_labels);
fclose(fid_csv);
