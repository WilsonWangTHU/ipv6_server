% ----------------------------------------------------------------------
% In this code, the program will read the ping output of the data
%
% Written by Tingwu Wang, for his bachelor thesis
% ----------------------------------------------------------------------

function [data, counter] = iperfReader(fileDir, numData, threshold)

    % initializing the variables
    data = zeros(numData, 1);
    fid = fopen(fileDir, 'r');
    counter = 0;
    
    
    while ~feof(fid)
        tline = fgetl(fid);
        startPos = strfind(tline, 'MBytes  ');
        endPos = strfind(tline, 'Mbits/sec');
        if isempty(endPos) || isempty(startPos)
            continue
        end
        
        counter = counter + 1;
        data(counter) = str2double(tline(startPos + 8: endPos - 2));
        if data(counter) > threshold
            counter = counter - 1;
        end
        if numData <= counter
            break;
        end
        data = data(1:counter);
    end
end
