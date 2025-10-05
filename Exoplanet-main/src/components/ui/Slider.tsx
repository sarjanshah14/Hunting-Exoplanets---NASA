import { InputHTMLAttributes } from 'react';

interface SliderProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
  showValue?: boolean;
  suffix?: string;
}

export function Slider({ label, showValue = true, suffix = '', className = '', ...props }: SliderProps) {
  return (
    <div className="w-full">
      {label && (
        <div className="flex justify-between items-center mb-2">
          <label className="text-sm font-medium text-gray-300">{label}</label>
          {showValue && (
            <span className="text-sm text-cyan-400 font-mono">
              {props.value} {suffix}
            </span>
          )}
        </div>
      )}
      <input
        type="range"
        className={`w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider ${className}`}
        {...props}
      />
      <style>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          width: 18px;
          height: 18px;
          background: linear-gradient(135deg, #06b6d4, #3b82f6);
          border-radius: 50%;
          cursor: pointer;
          box-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
          transition: all 0.2s;
        }
        .slider::-webkit-slider-thumb:hover {
          transform: scale(1.2);
          box-shadow: 0 0 15px rgba(6, 182, 212, 0.8);
        }
        .slider::-moz-range-thumb {
          width: 18px;
          height: 18px;
          background: linear-gradient(135deg, #06b6d4, #3b82f6);
          border-radius: 50%;
          border: none;
          cursor: pointer;
          box-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
          transition: all 0.2s;
        }
        .slider::-moz-range-thumb:hover {
          transform: scale(1.2);
          box-shadow: 0 0 15px rgba(6, 182, 212, 0.8);
        }
      `}</style>
    </div>
  );
}
