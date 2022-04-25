
ptCloud = pcread('ply-results/cars/000033_204546.ply');
pointscolor=uint8(zeros(ptCloud.Count,3));
pointscolor(:,1)=128;
pointscolor(:,2)=128;
pointscolor(:,3)=128;

%c = unique(ptCloud.Intensity);

for i = 1:ptCloud.Count
    if (ptCloud.Intensity(i) ~= 0)
        pointscolor(i,1)=0;
        pointscolor(i,2)=255;
        pointscolor(i,3)=0;
    end
end

pcshow(ptCloud.Location, pointscolor);

%{
for k=0:1553
    x = num2str(k);
    if k < 10
        result_str = strcat('results/00000',x,'.ply');
    elseif k < 100
        result_str = strcat('results/0000',x,'.ply');
    elseif k < 1000
        result_str = strcat('results/000',x,'.ply');
    else
        result_str = strcat('results/00',x,'.ply');
    end

    ptCloud = pcread(result_str);
    pcshow(ptCloud);
    fprintf('%i\n', k)
    pause(0.05)
end
%}
