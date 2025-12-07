import { useCallback, useState } from 'react';
import { Upload } from 'lucide-react';
import { cn } from '@/lib/utils';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  disabled?: boolean;
}

export const FileUpload = ({ onFileSelect, disabled }: FileUploadProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragging(true);
    } else if (e.type === "dragleave") {
      setIsDragging(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files[0] && !disabled) {
      handleFile(files[0]);
    }
  }, [disabled]);

  const handleFile = (file: File) => {
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
      onFileSelect(file);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      handleFile(files[0]);
    }
  };

  return (
    <div
      className={cn(
        "relative rounded-xl border-2 border-dashed transition-all duration-300 cursor-pointer overflow-hidden",
        isDragging ? "border-primary bg-primary/5 scale-105" : "border-border bg-card hover:border-primary/50 hover:bg-card/80",
        disabled && "opacity-50 cursor-not-allowed"
      )}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <label className={cn("block p-12 text-center", disabled && "cursor-not-allowed")}>
        <input
          type="file"
          className="hidden"
          accept="image/jpeg,image/png"
          onChange={handleFileInput}
          disabled={disabled}
        />
        
        {preview ? (
          <div className="space-y-4">
            <img 
              src={preview} 
              alt="Preview" 
              className="max-h-64 mx-auto rounded-lg shadow-glow"
            />
            <p className="text-sm text-muted-foreground">
              Dosya yüklendi • Sınıflandırmak için butona tıklayın
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="mx-auto w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
              <Upload className="w-8 h-8 text-primary" />
            </div>
            <div className="space-y-2">
              <p className="text-lg font-medium text-foreground">
                Astronomi fotoğrafı yükleyin
              </p>
              <p className="text-sm text-muted-foreground">
                Sürükle-bırak yapın veya tıklayarak dosya seçin
              </p>
              <p className="text-xs text-muted-foreground">
                JPG veya PNG formatında
              </p>
            </div>
          </div>
        )}
      </label>
    </div>
  );
};
