import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { FileUpload } from '@/components/FileUpload';
import { ClassificationResult } from '@/components/ClassificationResult';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, Sparkles } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

const Index = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<{
    debugImageBase64: string;
    objectCount: number;
    classCounts: Record<string, number>;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const handleClassify = async () => {
    if (!selectedFile) {
      toast({
        title: "Dosya seçilmedi",
        description: "Lütfen bir astronomi fotoğrafı yükleyin",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('image', selectedFile);

      // Gerçek API bağlantısı (localhost:5000)
      const response = await fetch('http://127.0.0.1:5000/classify', {
        method: 'POST',
        body: formData,
      });


      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `API hatası: ${response.statusText}`);
      }
      
      // Sunucudan gelen JSON verisini al
      const data = await response.json();

      setResult({
        debugImageBase64: data.debug_image_base64,
        objectCount: data.object_count,
        classCounts: data.class_counts,
      });

      toast({
        title: "Sınıflandırma tamamlandı",
        description: `${data.object_count} nesne tespit edildi`,
      });

    } catch (err) {
      console.error('Classification error:', err);
      let errorMessage = 'Bir hata oluştu. Lütfen farklı bir görüntü deneyin.';
      if (err instanceof Error) {
        errorMessage = err.message;
      }
      
      if (err instanceof TypeError && err.message === 'Failed to fetch') {
        errorMessage = "API sunucusuna bağlanılamadı. Backend'in (image_service.py) çalıştığından ve CORS ayarlarının yapıldığından emin olun.";
      }

      setError(errorMessage);
      
      toast({
        title: "Hata",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 space-y-4 animate-in fade-in slide-in-from-top duration-700">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-4">
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">Yapay Zeka Destekli</span>
          </div>
          <h1 className="text-5xl font-bold text-foreground tracking-tight">
            Astronomik Nesne Sınıflandırıcı
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Bir astronomi fotoğrafı (.jpg, .png) yükleyin ve yapay zeka modelimin 
            görüntüdeki nesneleri nasıl sınıflandırdığını görün.
          </p>
        </div>

        {/* Upload Section */}
        <div className="max-w-2xl mx-auto mb-8 animate-in fade-in slide-in-from-bottom duration-700">
          <FileUpload 
            onFileSelect={setSelectedFile} 
            disabled={isLoading}
          />
          
          <div className="mt-6 text-center">
            <Button
              onClick={handleClassify}
              disabled={!selectedFile || isLoading}
              variant="stellar"
              size="lg"
              className="min-w-[200px] h-14 text-lg"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  İşleniyor...
                </>
              ) : (
                'SINIFLANDIR'
              )}
            </Button>
            
            {isLoading && (
              <p className="text-sm text-muted-foreground mt-4 animate-pulse">
                Görüntü işleniyor, bu işlem birkaç dakika sürebilir...
              </p>
            )}
          </div>
        </div>

        {/* Error State */}
        {error && (
          <Alert variant="destructive" className="max-w-2xl mx-auto mb-8 animate-in fade-in duration-500">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Results */}
        {result && (
          <ClassificationResult
            imageBase64={result.debugImageBase64}
            objectCount={result.objectCount}
            classCounts={result.classCounts}
          />
        )}
      </div>
    </div>
  );
};

export default Index;