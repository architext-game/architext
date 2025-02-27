import clsx from "clsx";

interface BenefitProps {
  title: string;
  subtitle: string;
  visual: React.JSX.Element;
  className?: string;
  reverse?: boolean;
}

export const Benefit: React.FC<BenefitProps> = ({ title, subtitle, visual, className, reverse=false }) => {
  return (
    <div className={clsx("flex max-w-4xl mx-auto", className, reverse && "flex-row-reverse")}>
      <div className="flex w-2/5 justify-center items-center">{ visual }</div>
      <div className="flex w-3/5 flex-col gap-5">
        <div className="text-4xl">{ title }</div>
        <div>{ subtitle }</div>
      </div>
    </div>
  )
};

