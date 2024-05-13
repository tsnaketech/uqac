package stev.kwikemart;

public abstract class PaperRollException extends StoreException {
   private static final long serialVersionUID = 1L;

   public PaperRollException(String message) {
      super(message);
   }

   public static class OutOfPaperException extends StoreException {
      private static final long serialVersionUID = 1L;
      public static final PaperRollException.OutOfPaperException instance = new PaperRollException.OutOfPaperException();

      private OutOfPaperException() {
         super("The roll has run out of paper");
      }
   }
}
