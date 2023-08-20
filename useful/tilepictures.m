function tilepictures(fignames,tile,crop,filename,text,textpos,fontsize)

%% Tile jpg/png figures (e.g. mode plots)
%
% Inputs:
% tile: [nh,nw] tile
% crop: [1,4] crop in pixels
% filename: name of saved png file
% text: cell with text strings
% textpos: position of text within each subfig
% fontsize: size of text

%%

if nargin<5
    text={};
end
    
if nargin<6
    textpos={};
end
    
if nargin<7
    fontsize=60;
end
    
k=0;
for k1=1:tile(1)
    for k2=1:tile(2)
        k=k+1;
        if k>length(fignames{k}); continue; end
        [I{k1,k2},cmap]=imread(fignames{k});
        I{k1,k2}=ind2rgb(I{k1,k2},cmap);

        [s1,s2,c]=size(I{k1,k2});
        range1=(crop(2)+1):(s1-crop(1));
        range2=(crop(3)+1):(s2-crop(4));

        if isempty(range1)
            error('Crop 1 too large');
        end

        if isempty(range2)
            error('Crop 2 too large');
        end

        I{k1,k2}=I{k1,k2}(range1,range2,:);

    end
end

I_all=cell2mat(I);

% imshow(I_all)
% tilefigs

%%

close all

[s1,s2,c]=size(I{1});

I_all_text=I_all;

% textpos=[0 0];
k=0;
for k1=1:tile(1)
    for k2=1:tile(2)
        k=k+1;
        if k>length(fignames{k}); continue; end

        position=[s1*textpos(1)+(k1-1)*s1,s2*textpos(2)+(k2-1)*s2];
        position=flip(position);
        I_all_text = insertText(I_all_text,position,text{k},'FontSize',fontsize,'TextColor','black','BoxColor','white','BoxOpacity',0.0);
    end
end
% I_all_text = insertText(I_all_text,position,letters{k},'FontSize',60,'TextColor','black','BoxColor','white','BoxOpacity',0.0);

figure();
imshow(I_all_text)

% tilefigs

% return
imwrite(I_all_text,[filename '.png']);

