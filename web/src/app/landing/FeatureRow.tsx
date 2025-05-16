import clsx from "clsx";

interface FeatureRowProps {
  children: React.ReactNode;
  className?: string;
}

export const FeatureRow: React.FC<FeatureRowProps> = ({ children, className }) => {
  return (
    <div className={clsx("flex flex-col sm:flex-row gap-20 sm:gap-8", className)}>
      {children}
    </div>
  )
};

interface FeatureRowItemProps {
  icon: string,
  title: string,
  description: string,
}

export const FeatureRowItem: React.FC<FeatureRowItemProps> = ({
  icon, title, description
}) => {
  return (
    <div className="flex flex-col gap-4 text-center text-xl">
      <div className="text-7xl">
        {icon}
      </div>
      <div className="flex flex-col gap-2">
        <div className="font-bold">
          {title}
        </div>
        <div className="text-base opacity-80">
          {description}
        </div>
      </div>
    </div>
  )
};


